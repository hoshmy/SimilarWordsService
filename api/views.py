from django.http import HttpResponse
import json
from time import time
import copy

from configurations import configuration
from utilities.similar_words_dictionary_parser import SimilarWordsDictionaryParser
from utilities.stats_calculator import StatsCalculator

parser = SimilarWordsDictionaryParser()
number_of_words_in_dictionary, similar_words_dictionary = parser.parse(configuration.path_to_dictionary_file)


def similar(request):
    begin = time()
    if request.method == 'GET':
        if 'word' in request.GET:
            # Fetched received parameter and format is
            query_word = request.GET['word']
            clean_query_word = query_word.rstrip('\n').strip().lower()

            # Sorted word will be used as the information key
            sorted_word = ''.join(sorted(clean_query_word))

            ret_dict = {'similar': []}  # Default response in case there aren't any similar words in the dictionary
            if sorted_word in similar_words_dictionary:
                ret_dict = similar_words_dictionary[sorted_word]

                # Omit the queried word if present
                if clean_query_word in ret_dict['similar']:
                    ret_dict = copy.deepcopy(ret_dict)
                    ret_dict['similar'].remove(clean_query_word)

            json_string = json.dumps(ret_dict)
            total_time = time() - begin
            StatsCalculator.add_request_stat(total_time)
            return HttpResponse(json_string)

    # Default response
    return HttpResponse('')


def stats(request):
    if request.method == 'GET':
        # Fetch Statistics
        stats_dict = StatsCalculator.get_stats()

        # Add to the statistics the totalWords information
        stats_dict['totalWords'] = number_of_words_in_dictionary
        json_string = json.dumps(stats_dict)
        return HttpResponse(json_string)

    # Default response
    return HttpResponse('')
