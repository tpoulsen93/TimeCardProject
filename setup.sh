#!/bin/bash

#Author: Taylor Poulsen
#Date: January 2021

echo "compile java code..."
echo
javac TimeCard.java GenerateTimeCards.java

echo "install program to convert excel spreadsheet to csv..."
echo
sudo apt-get install xlsx2csv

echo "Should be ready to rumble.... I hope..."
