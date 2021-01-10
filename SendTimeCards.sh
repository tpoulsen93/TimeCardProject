#!/bin/bash

#Author: Taylor Poulsen
#Date: January 2021
#Purpose: Automate some of my weekly payroll tasks for Poulsen Concrete Contractors


#Print usage if incorrect # of arguments provided
if [ $# -lt 2 ] || [ $# -gt 3 ]; then
    echo Usage:   $0 '<start date> <payday> [<# of days in pay period>]'
    echo Date format: mm-dd-yy
    exit 1
fi

#these 2 variables are hardcoded and will have to be updated from time to time using the updateHardcodedVariables script
#add the actual address of the file here, will have to be updated once per year
spreadSheet=~/payroll/Book1.xlsx  
#employee count will have to change each time employees are added or lost...
eCount=1                            

startDate=$1                #the start date of the payroll to be computed
payDay=$2                   #the date of the payday
csv=$payDay/tmp.csv         #name of temporary csv file that will be overwritten over and over during program execution

if [ $# -gt 2 ]; then   #if pay period length isn't provided, default is 7
    payPeriodLength=$3
else
    payPeriodLength=0
fi

b64temp=base64_template.txt


#make a directory for copies of all of the TimeCards
if [ -e $payDay ]; then
    rm -fr $payDay
fi
mkdir $payDay

#loop through the sheets creating temporary csv's, generating time cards, and sending them
for (( i=1; i<( $eCount + 1 ); i++ ))
do
    timeCard=$payDay/TimeCard_$i.txt
    #generate the template for the base64
if [ ! -e $b64temp ]; then
    echo "Content-Type: application;" >> $b64temp
    echo "Content-Transfer-Encoding: base64" >> $b64temp
    echo "Content-Disposition: attachment; filename=\"TimeCard.txt\"" >> $b64temp
fi

    #convert the spreadsheet to a csv
    xlsx2csv -s $i $spreadSheet $csv

    #generate timecard from csv
    if [ -e $csv ]; then
        java GenerateTimeCards $csv $startDate $payDay $payPeriodLength > $timeCard
        rm -f $csv
    else
        echo No csv found.
        exit 1
    fi

    #get info from the first few lines of the timecard
    phone=$(head -n 1 $timeCard)
    email=$(head -n 2 $timeCard | tail -1)
    name=$(head -n 3 $timeCard | tail -1)

    #remove the first 2 lines from the timecard
    sed -i '1,2d' $timeCard

    #generate the template for the base64 file
    echo "Subject: Time Card for $name" >> $b64temp
    echo "Content-Type: application;" >> $b64temp
    echo "Content-Transfer-Encoding: base64" >> $b64temp
    echo "Content-Disposition: attachment; filename=\"TimeCard.txt\"" >> $b64temp

    #convert the timecard to base64 and append to the template to be sent as an attachment in the email
    base64 $timeCard >> $b64temp

    #send the timecard and delete the base64 file
    sendmail $email < $b64temp
    rm -f $b64temp
    echo "A time card was sent to $name"

    #send text message alerting recipient that their timecard has been sent
    echo "Your time card for the pay period starting on $startDate has been sent to $email" | sendmail $phone
    echo "Direct Deposit will be scheduled for $payDay" | sendmail $phone
    echo "If you see any errors, or have any questions, please text me at 208-350-0006" | sendmail $phone
    echo "$name was alerted via text message"
done