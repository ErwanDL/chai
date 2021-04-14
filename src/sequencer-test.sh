#! /bin/bash

echo "sequencer-test.sh start"

HELP_MESSAGE=$'Usage: ./sequencer-test.sh
Depends on environment variable settings
export data_path=.../data  # Or a new directory path as desired'

if [ ! -f $data_path/train.sh ]; then
  echo "data_path environment variable should be set"
  echo "$HELP_MESSAGE"
  exit 1
fi

cd $data_path
echo "Starting test data translation"
# Change code in translate.sh to adjust OpenNMT parameters (like beam width)
./translate.sh

echo "sequencer-test.sh done"
echo
exit 0
