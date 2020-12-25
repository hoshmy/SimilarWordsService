#!/bin/bash

cd tests
echo "Generating tests files.."
python3 dictionary_generator.py

cd ..
echo "Starting tests - errors, if occur will be printed to stderr"
python3 -m tests.client_simulator
