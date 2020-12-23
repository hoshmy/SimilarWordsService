from django.http import HttpResponse
import json

from utilities.similar_words_dictionary_parser import SimilarWordsDictionaryParser
from configurations import configuration
from utilities.logger import Logger

parser = SimilarWordsDictionaryParser()
similar_words_dictionary = parser.parse(configuration.path_to_dictionary_file)


def similar(request):
    if request.method == 'GET':
        word = request.GET['word']  # TODO: check if missing
        ret_dict = {'similar': []}

        word = word.rstrip('\n').strip().lower()
        # sorted word will be used as the information key
        sorted_word = ''.join(sorted(set(word.lower())))
        if sorted_word in similar_words_dictionary:
            ret_dict = similar_words_dictionary[sorted_word]

        json_string = json.dumps(ret_dict)
        return HttpResponse(json_string)
