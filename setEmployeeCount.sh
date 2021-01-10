#!/bin/bash

#Author: Taylor Poulsen
#Date: January 2021

current=$(cat SendTimeCards.sh | grep eCount=)

if [ $# -eq 0 ] || [ $# -gt 2 ]; then
    echo "Usage: $0 <new employee count>"
    echo "Current employee count: $current"
    exit 0
fi

#change the eCount to the new value
sed -i s/^eCount=.*/eCount=$1/ SendTimeCards.sh
current=$(cat SendTimeCards.sh | grep eCount=)
echo "New employee count: $current"