#include <stdio.h>
#include <stdlib.h>
#include "error.h"

int main (int argc, char* argv[])
{
    //only the first argument matters, anything else is garbage

    char* fileName = argv[1];
    char phoneBuffer[255];

    FILE* file;
    file = fopen(fileName, "r");
    fscanf(file, "%s", phoneBuffer);    //get the phone email address off the first line of the time Card

    for (int i = 0; phoneBuffer[i]; i++)    //clean off line terminator
        if (phoneBuffer[i] == '\n')
            phoneBuffer[i] = 0;

    printf(stdout, "%s", phoneBuffer);  //print the phone number to standard out to be picked up by the script for the mailing step

    return 0;
}