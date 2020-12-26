import os


class Configuration:
    # path_to_dictionary_file should be relative to the project directory or an absolute full path
    path_to_dictionary_file = 'words_clean.txt'
    path_to_test_dictionary_file = 'tests/generated_dictionary.txt'

    @staticmethod
    def get_path_to_dictionary_file():
        if os.environ.get('test'):
            return Configuration.path_to_test_dictionary_file
        else:
            return Configuration.path_to_dictionary_file

