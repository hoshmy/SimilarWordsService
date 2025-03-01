import os
import sys

from utilities.logger import Logger
from configuration import Configuration


class SimilarWordsDictionaryParser:
    _number_of_lines = 0
    _number_of_words = 0

    @staticmethod
    def parse(path_to_file: str) -> (dict, int):
        # Reset previous runs
        similar_words_groups = {
            # 'aab': {'similar':['aba', 'aab', 'baa']},
            # sorted_word: {'similar':['all', 'similar','words']}
        }

        SimilarWordsDictionaryParser._do_parse(path_to_file, similar_words_groups)

        Logger.log(
            'Parsing {}: found {} unique words out of {} total words combined in {} similarities groups'.format(
                path_to_file, SimilarWordsDictionaryParser._number_of_words,
                SimilarWordsDictionaryParser._number_of_lines, len(similar_words_groups)))

        return SimilarWordsDictionaryParser._number_of_words, similar_words_groups

    @staticmethod
    def _do_parse(path_to_file: str, similar_words_groups: dict) -> None:

        try:
            if os.path.isfile(path_to_file):
                with open(path_to_file, 'r') as file:
                    for line_from_file in file:
                        SimilarWordsDictionaryParser._number_of_lines += 1
                        SimilarWordsDictionaryParser._add_word(line_from_file, similar_words_groups)
            else:
                Logger.log('File "{}" doesn\'t exists'.format(path_to_file), Logger.Level.FATAL)
        except IOError as e:
            Logger.log('I/O error({}): {}'.format(e.errno, e.strerror), Logger.Level.FATAL)
        except:  # handle other exceptions such as attribute errors
            Logger.log('Unexpected error: {}'.format(sys.exc_info()[0]), Logger.Level.FATAL)

    @staticmethod
    def _add_word(line_from_file: str, similar_words_groups: dict) -> None:
        # Remove ending \n
        # Remove ending \r  (For windows compatibility)
        # Remove trailing and leading white character
        # set to lower case - words meaning is case insensitive
        word = line_from_file.rstrip('\n').rstrip('\r').strip().lower()

        if word:
            # sorted word will be used as the information key
            sorted_word = ''.join(sorted(word.lower()))

            if sorted_word in similar_words_groups:
                # Filter out identical words
                if word not in similar_words_groups[sorted_word]['similar']:
                    similar_words_groups[sorted_word]['similar'].append(word)
                    SimilarWordsDictionaryParser._number_of_words += 1
                else:
                    Logger.log('Word duplication found for {}'.format(word))
            else:
                similar_words_groups[sorted_word] = {'similar': [word]}
                SimilarWordsDictionaryParser._number_of_words += 1
        else:
            # White characters line was found, ignore it
            pass


if __name__ == '__main__':
    num_of_words, parsed_dict = SimilarWordsDictionaryParser.parse(Configuration.get_path_to_dictionary_file())
