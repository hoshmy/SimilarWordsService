from django.http import HttpResponse
import json

from utilities.similar_words_dictionary_parser import SimilarWordsDictionaryParser
from configurations import configuration


parser = SimilarWordsDictionaryParser()
parser.parse(configuration.path_to_dictionary_file)


def similar(request):
    return HttpResponse("Hello, world. You're at the api/v1/similar")
