import os
import sys

from utilities.logger import Logger


class SimilarWordsParser:
    def __init__(self, path_to_file: str):
        self._path_to_file = path_to_file
        self._similar_words_groups = {
            # 'aab': {'similar':['aba', 'aab', 'baa']},
            # sorted_word: {'similar':['all', 'similar','words']}
        }
        self._number_of_words = 0
        self._number_of_lines = 0
        self._parse()
        Logger.log(
            'Parsing {}: found {} unique words out of {} total words combined in {} similarities groups'.format(
                self._path_to_file, self._number_of_words, self._number_of_lines, len(self._similar_words_groups)))

    def _parse(self):
        try:
            if os.path.isfile(self._path_to_file):
                with open(self._path_to_file, 'r') as file:
                    for line in file:
                        self._number_of_lines += 1
                        self._add_word(line)
            else:
                Logger.log('File "{}" doesn\'t exists'.format(self._path_to_file), Logger.Level.FATAL)
        except IOError as e:
            Logger.log('I/O error({}): {}'.format(e.errno, e.strerror), Logger.Level.FATAL)
            sys.exit(-1)
        except:  # handle other exceptions such as attribute errors
            Logger.log('Unexpected error: {}'.format(sys.exc_info()[0]), Logger.Level.FATAL)
            sys.exit(-1)

    def _add_word(self, line_from_file: str):
        # Remove ending \n
        # Remove trailing and leading white character
        # set to lower case - words meaning is case insensitive
        word = line_from_file.rstrip('\n').strip().lower()

        if word:
            # sorted word will be used as the information key
            sorted_word = ''.join(sorted(set(word.lower())))

            if sorted_word in self._similar_words_groups:
                # Filter out identical words
                if word not in self._similar_words_groups[sorted_word]['similar']:
                    self._similar_words_groups[sorted_word]['similar'].append(word)
                    self._number_of_words += 1
                else:
                    Logger.log('Word duplication found for {}'.format(word))
            else:
                self._similar_words_groups[sorted_word] = {'similar': [word]}
                self._number_of_words += 1
        else:
            # White characters line was found, ignore it
            pass


if __name__ == '__main__':
    parser = SimilarWordsParser('words_clean.txt')
