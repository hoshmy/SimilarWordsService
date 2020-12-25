import os
from itertools import permutations
import random
import string
import json

# Generator configuration
number_of_words = 500001
file_name_prolog = 'generated'
max_number_of_similar_words = 10
max_word_size = 20


class DictionaryGenerator:
    _generated_words = []
    _answers = {
        # 'aab': {'similar':['aba', 'aab', 'baa']},
        # sorted_word: {'similar':['all', 'similar','words']}
    }

    @staticmethod
    def create() -> None:
        DictionaryGenerator._generate(num_of_words=number_of_words)
        print('finished generation')
        DictionaryGenerator._prepare_files(file_name=file_name_prolog)
        print('finished files writing')

    @staticmethod
    def _generate(num_of_words: int) -> None:
        DictionaryGenerator._generated_words = []
        DictionaryGenerator._answers = {}
        num_of_words_to_generate = num_of_words
        generated_sorted_words_set = set()

        while num_of_words_to_generate > 0:
            num_of_similar_words = random.randint(1, max_number_of_similar_words)
            current_word = DictionaryGenerator._get_random_string()
            generated_word_key = ''.join(sorted(current_word))

            # Skip handled permutations
            if generated_word_key in generated_sorted_words_set:
                continue
            else:
                generated_sorted_words_set.add(generated_word_key)

            # foreach generated word - prepare similar words according to random parameters
            current_permutation_avoid_duplication = {}
            for permutation in permutations(current_word):
                # Duplication handling
                if permutation in current_permutation_avoid_duplication:
                    continue
                else:
                    current_permutation_avoid_duplication[permutation] = None

                permutation_string = ''.join(permutation)

                # Save the generated similar word and manage the counting
                if num_of_similar_words and num_of_words_to_generate:
                    DictionaryGenerator._generated_words.append(permutation_string)
                    if generated_word_key in DictionaryGenerator._answers:
                        if permutation_string not in DictionaryGenerator._answers[generated_word_key]['similar']:
                            DictionaryGenerator._answers[generated_word_key]['similar'].append(permutation_string)
                        else:
                            continue  # Skip the indexing substraction
                    else:
                        DictionaryGenerator._answers[generated_word_key] = {'similar': [permutation_string]}
                    num_of_similar_words -= 1
                    num_of_words_to_generate -= 1
                else:
                    break

    @staticmethod
    def _prepare_files(file_name: str) -> None:
        # Prepare dictionary
        dictionary_file_name = '{}_dictionary.txt'.format(file_name)
        words = DictionaryGenerator._generated_words.copy()  # Work on a local copy

        # Delete file - to allow new copy
        if os.path.isfile(dictionary_file_name):
            os.remove(dictionary_file_name)

        # Fetch a random word and write it to the dictionary
        while words:
            rand_index = random.randint(0, len(words)-1)

            with open(dictionary_file_name, 'a') as file:
                file.write('{}\n'.format(words[rand_index]))

            del words[rand_index]

        # Prepare answers dictionary
        answers_file_name = '{}_answers.txt'.format(file_name)
        with open(answers_file_name, 'w') as file:
            file.write(json.dumps(DictionaryGenerator._answers))

    @staticmethod
    def _get_random_string(length=-1) -> str:
        if length < 0:
            length = random.randint(1, max_word_size)
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str


if __name__ == '__main__':
    DictionaryGenerator.create()
