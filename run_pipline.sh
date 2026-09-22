#!/bin/bash

if [ -d "data/" ]; then
    rm -r data/
fi
echo -e "Starting the pipeline... $(date +%t%F%t%T)" >> pipeline.log
echo -e  "Generating data...\\n"
python  Script/generate_data.py

echo -e "Start generation data $(date +%t%F%t%T)" >> pipeline.log
if [ $? -ne 0 ]; then
    echo -e "Data generation failed. Exiting."
    exit 1
fi
echo -e "Ending generation data $(date +%t%F%t%T)" >> pipeline.log

echo -e "Generating data completed successfully.\\n"

echo -e "Start validation data $(date +%t%F%t%T)" >> pipeline.log
echo -e "Validating data...\\n"
python Script/validate.py

if [ $? -ne 0 ]; then
    echo "Validation failed. Exiting."
    exit 2
fi
echo -e "Ending validation data $(date +%t%F%t%T)" >> pipeline.log

echo -e "Validation completed successfully.\\n"

echo -e "Start transformation data $(date +%t%F%t%T)" >> pipeline.log
echo -e "Transforming data...\\n"

python Script/transform.py
if [ $? -ne 0 ]; then
    echo "Transformation failed. Exiting."
    exit 3
fi
echo -e "Ending transformation data $(date +%t%F%t%T)" >> pipeline.log

echo -e "Transformation completed successfully.\\n" 

echo -e "Ending the pipeline... $(date +%t%F%t%T)" >> pipeline.log