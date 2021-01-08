#!/bin/bash

#Author: Taylor Poulsen
#Date: January 2021
#Purpose: Automate some of my weekly payroll tasks for Poulsen Concrete Contractors


#Print usage if incorrect # of arguments provided
if [ $# -lt 3 ] || [ $# -gt 4 ]; then
    echo Usage:   $0 '<start date> <payday> [<# of days in pay period>]'
    echo Date format: mm-dd-yy
    exit 1
fi

#these 2 variables are hardcoded and will have to be updated from time to time
spreadSheat="./Book1.xlsx"  #add the actual address of the file here (hardcoded isn't ideal but will only have to be updated once per year)
eCount=7                    #employee count will also be hard coded and have to change each time employees are gained or lost...


startDate=$1                #the start date of the payroll to be computed
payDay=$2                   #the date of the payday
csv=tmp.csv

if [ $# -gt 4 ]; then   #if pay period length isn't provided, default is 7
    payPeriodLength=$3
else
    payPeriodLength=0
fi

mkdir $1    #make directory with the name of the startDate
cd $1       #change to the directory to then fill with TimeCard files


#loop through the sheets creating temporary csv's, generating time cards, and sending them
for (( i=0; i<$eCount; i++ ))
do
    xlsx2csv -s "$i $spreadSheat $csv"   #convert the spreadsheet to a csv

if [ -e tmp.csv ]; then
    java GenerateTimeCards "$csv $startDate $payDay $payPeriodLength" > "TimeCard_$i".txt #generate timecard from csv
else
    echo No csv was generated.
    exit 1
fi

done