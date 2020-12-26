# SimilarWordsService
Palo Alto Task
 
 **Service requirements**
 A small web service for printing similar words in the English language.
Two words w_1 and w_2 are considered similar if w_1 is a letter permutation of w_2 (e.g., "stressed" and "desserts").

We provide a DB of the English dictionary you should work with. Please find it in the attached archive. The service can expect the DB (the txt file) to be in the local directory with the same name.

The web service should listen on port 8000 and support the following two HTTP endpoints:

GET /api/v1/similar?word=stressed
Returns all words in the dictionary that have the same permutation as the word "stressed". The word in the query should not be returned.

The result format is a JSON object as follows:
{
    similar:[list,of,words,that,are,similar,to,provided,word]
}

For example:
http://localhost:8000/api/v1/similar?word=apple
{"similar":["appel","pepla"]}

GET /api/v1/stats
Return general statistics about the program:
Total number of words in the dictionary
Total number of requests (not including "stats" requests)
Average time for request handling in nanoseconds (not including "stats" requests)

The output is a JSON object structured as follows:
{
    totalWords:int
    totalRequests:int
    avgProcessingTimeNs:int
}

For example:
http://localhost:8000/api/v1/stats
{"totalWords":351075,"totalRequests":9,"avgProcessingTimeNs":45239}

 
 **Algorithm**
 The dictionary file is parsed on while the system boot.
 the parser reads each line (word) and build a python dict (a hash data structure) with the following structure:
 
 similar_words_groups = {
    'aab': {'similar':['aba', 'baa']},
    sorted_word: {'similar':['all', 'similar','words']}
 }
 
 The dictionary key is a string - that is a sorted permutation of its underlying words
 The value is another python dictionary formatted the sane as the response JSON from the api/v1/similar Get request
 
 Upon receiving a similar request - the api/view.py handles the request - it sorts the parameter it received.
 Then it fetches the answer from the dictionary the parser prepared. When necessary it omits the queried word.
 
 For each similar GET request - the process tie is measured and delivered ti the StatsCalculator object.
   Adding a timing measurement - only put the time sample in a synchronized queue.
   The StatsCalculator has a worker thread that periodically empties the queue and counts number of requests, and sums up all the processing time    
 
 **Environment**
  - The service was developed in python3 (Tested with python 3.8.5 and 3.7.4) using the Django web framework (https://www.djangoproject.com/)
  - Django version 3.1.4 (Latest, for 12.2020)
  - Linux Ubuntu 20.04

**Installation**
  - sudo apt -y install python3.8
    Can be verified using: python3.8 --version. Answer: Python 3.8.5
  - sudo apt -y install python3-pip
  - python3.8 -m pip install Django
    Can be verified using python3.8 -c "import django; print(django.get_version())"
    Answer: 3.1.4
    
    Note: It is most likely that any python 3.7+ version and django 3.1+ version could work just fine
 
**Run the service**
cd to the project's folder
chmod +x run_service.sh
./run_service

**Run tests**
The tests are dependant on tests generated files: tests/generated_dictionary.txt and test/generated_answers.txt
These files should be generated once before running the tests. Regeneration will run previous files with new random results
  - Generate the tests files once by running generate_test_files.sh

Once the tests files exists, run the tests:  
  - Run service as test
      * cd to the project's folder
      * chmod +x run_test.sh
      * ./run_service_test.sh
  - Run clients test:
      * Open another terminal
      * cd to the project's folder
      * ./run_test.sh
  
Tests errors, if occurred will be printed to stderr.
If no errors detected - no prints will be done
  
**Configuration**
In the <project folder>/configuration.py where the variable path_to_dictionary_file can be changed to point to another file
Its value must be a relative path starting from <project folder> or an absolute complete path

**Code highlights**
  - manage.py is the "main" file - which implements the system entry point
  - configuration.py - modest configuration allowing easy dictionary swapping
  - api/views.py - implements the callback methods that handle the GET requests
  - utilities/
    * running_orchestrator.py - a small static-interface only class that allows easy signals whether the system is running or not
    * similar_words_dictionary_parser.py - static-interface only class that implements the dictionary parser
    * stats_calculator.py - static-interface only class that implements the synchronized accumulating and calculations of stats
    * logger.py - static-interface only class that implements log
  - tests/
    * dictionary_generator.py - generates a synthetic dictionary for testings
    * client_simulator.py - runs multiple clients instances that sends GET requests and verify response correctness

**Author**
  - Itamar Hoshmand
  - hoshmy@gmail.com
  - +972503401881