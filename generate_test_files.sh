#!/bin/bash

cd tests
echo "Generating tests files"
python3.8 dictionary_generator.py
echo "Finished"
cd ..