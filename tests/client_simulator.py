import random
import requests
import json
import threading
import time

from utilities.logger import Logger

# simulator configuration
client_iterations = 100000
client_sleep_time = 1e-6
number_of_clients = 20
expected_answers_file = 'generated_answers.txt'
clients_launch_time_delta = 1
server_url = 'http://127.0.0.1:8000/api/v1/similar'


def client_thread(answers_dict):
    for _ in range(client_iterations):
        # Fetch a random word from all possibilities
        rand_answer_key = random.choice(list(answers_dict.keys()))
        rand_list_of_similar_keys = answers_dict[rand_answer_key]['similar']
        current_word = random.choice(rand_list_of_similar_keys)

        # Send a GET request (blocking) to the Server
        response = requests.get(server_url, {'word': current_word})
        response_dict = json.loads(response.text)

        # Prepare the correct expected answer - omitting the queried word
        answer_array_without_query_word = list(answers_dict[rand_answer_key]['similar'])
        # answer_array_without_query_word.remove(current_word)

        # Compare response and expected answer - log if an error was found
        if not _is_arrays_content_same(response_dict['similar'], answer_array_without_query_word):
            Logger.log('Error in answer given for word {}, returned similar_words: {}, expected similar words {}'.
                       format(current_word, response_dict['similar'], answer_array_without_query_word))

        # Yield CPU to allow other threads to work
        time.sleep(client_sleep_time)


def _is_arrays_content_same(arr1, arr2):
    # Return True if the 2 arrays of string are of the same length and have the same set of values
    if len(arr1) != len(arr2):
        return False

    for entry in arr1:
        if entry not in arr2:
            return False

    return True


if __name__ == '__main__':
    threads = []
    answers = {}

    # Parse the answers dict
    with open(expected_answers_file, 'r') as file:
        answers = json.loads(file.read())

    # Launch each client in his own thread
    for i in range(number_of_clients):
        Logger.log('Launching client #{}'.format(i), Logger.Level.DEBUG)
        curr_thread = threading.Thread(target=client_thread, args=(answers,), daemon=True)
        curr_thread.start()
        threads.append(curr_thread)
        time.sleep(clients_launch_time_delta)

    # join all threads
    for thread in threads:
        thread.join()

    Logger.log('{} client finished working'.format(number_of_clients))
