#!/bin/bash

#Author: Taylor Poulsen
#Date: January 2021

echo "compile java code..."
echo
javac *.java
echo

echo "install xlsx2csv to convert excel spreadsheet to csv..."
echo
sudo apt-get install xlsx2csv
echo

echo "install sendmail to send texts and emails"
echo
sudo apt-get install ssmtp
echo

echo
echo "Look up how to configure ssmtp and do it."
echo "Then you should be ready to rumble.... I hope..."
