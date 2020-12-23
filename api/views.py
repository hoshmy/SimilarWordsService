from django.http import HttpResponse
import json
from time import time

from configurations import configuration
from utilities.similar_words_dictionary_parser import SimilarWordsDictionaryParser
from utilities.logger import Logger
from utilities.stats_calculator import StatsCalculator

parser = SimilarWordsDictionaryParser()
number_of_words_in_dictionary, similar_words_dictionary = parser.parse(configuration.path_to_dictionary_file)


def similar(request):
    begin = time()
    if request.method == 'GET':
        if 'word' in request.GET:
            word = request.GET['word']  # TODO: check if missing
            ret_dict = {'similar': []}

            word = word.rstrip('\n').strip().lower()
            # sorted word will be used as the information key
            sorted_word = ''.join(sorted(word.lower()))
            if sorted_word in similar_words_dictionary:
                ret_dict = similar_words_dictionary[sorted_word]

            json_string = json.dumps(ret_dict)
            total_time = time() - begin
            StatsCalculator.add_request_stat(total_time)
            return HttpResponse(json_string)
    return HttpResponse('')


def stats(request):
    if request.method == 'GET':
        stats_dict = StatsCalculator.get_stats()
        stats_dict['totalWords'] = number_of_words_in_dictionary
        json_string = json.dumps(stats_dict)
        return HttpResponse(json_string)

    return HttpResponse('')
