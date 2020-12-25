import random
import requests
import json
import threading
import time

from utilities.logger import Logger

# Simulator configuration
client_iterations = 100000
client_sleep_time = 1e-6
number_of_clients = 20
expected_answers_file = 'generated_answers.txt'
clients_launch_time_delta = 1
server_url = 'http://127.0.0.1:8000/api/v1/similar'
reconnection_time_delta = 5


def _client_send_request_blocking(word: str) -> requests.Response:
    # Send a GET request (blocking) to the Server
    response = None
    try:
        response = requests.get(server_url, {'word': word})
    except requests.exceptions.ConnectionError:
        Logger.log('Server is unavailable, wait and try later again')
        time.sleep(reconnection_time_delta)

    return response


def _client_compare_response_and_expected_results(
        response: requests.Response, answers_dict: dict, rand_answer_key: str, key_permutation: str) -> None:
    response_dict = {}
    if response and response.text:
        response_dict = json.loads(response.text)

        # Prepare the correct expected answer - omitting the queried word
        correct_list_of_all_similar_words = list(answers_dict[rand_answer_key]['similar'])
        if key_permutation in correct_list_of_all_similar_words:
            correct_list_of_all_similar_words.remove(key_permutation)

        # Compare response and expected answer - log if an error was found
        if not _is_arrays_content_same(response_dict['similar'], correct_list_of_all_similar_words):
            Logger.log('Error in answer given for word {}, returned similar_words: {}, expected similar words {}'.
                       format(key_permutation, response_dict['similar'], correct_list_of_all_similar_words))


def client_thread(answers_dict: dict, answers_keys_list: list) -> None:
    for _ in range(client_iterations):
        # Fetch a random key from all possibilities and shuffle it (creating a similar word)
        rand_answer_key = random.choice(answers_keys_list)
        rand_answer_key_list = list(rand_answer_key)
        random.shuffle(rand_answer_key_list)  # In place shuffling
        key_permutation = ''.join(rand_answer_key_list)

        response = _client_send_request_blocking(key_permutation)
        _client_compare_response_and_expected_results(response, answers_dict, rand_answer_key, key_permutation)

        time.sleep(client_sleep_time)  # Yield CPU to allow other threads to work


def _is_arrays_content_same(arr1: list, arr2: list) -> bool:
    # Return True if the 2 arrays of string are of the same length and have the same set of values
    if len(arr1) != len(arr2):
        return False

    for entry in arr1:
        if entry not in arr2:
            return False

    return True


def _parse_answers_file():
    answers_dict = {}
    with open(expected_answers_file, 'r') as file:
        try:
            answers_dict = json.loads(file.read())
        except json.JSONDecodeError:
            Logger.log('Error loading file {}, using default'.format(expected_answers_file))
            answers_dict = {}
    return answers_dict


def _launch_clients(answers: dict, all_answers_keys_list: list) -> list:
    # Launch each client in his own thread
    threads = []
    for i in range(number_of_clients):
        Logger.log('Launching client #{}'.format(i), Logger.Level.DEBUG)
        curr_thread = threading.Thread(target=client_thread, args=(answers, all_answers_keys_list), daemon=True)
        curr_thread.start()
        threads.append(curr_thread)
        time.sleep(clients_launch_time_delta)

    return threads


if __name__ == '__main__':
    answers = _parse_answers_file()
    # The keys are the sorted permutations. used to fetch a random test by clients
    all_answers_keys_list = list(answers.keys())
    threads = _launch_clients(answers, all_answers_keys_list)

    for thread in threads:
        thread.join()

    Logger.log('{} client finished working'.format(number_of_clients))
