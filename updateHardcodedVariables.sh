#!/bin/bash

#Author: Taylor Poulsen
#Date: January 2021

if [ $# -eq 0 ]; then
    echo "Usage: $0 <new employee count> [<new spreadsheet path>]"
fi

#change the eCount to the new value
sed -i \'s/eCount=.*/eCount=$1/\' SendTimeCards.sh

#change the spreadsheet path to the new path
if [ $# -gt 1 ]; then
    sed -i \'s/spreadSheet=.*/spreadSheet=$1/\' SendTimeCards.sh
fi