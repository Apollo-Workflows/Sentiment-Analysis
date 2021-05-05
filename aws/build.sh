#!/bin/bash
#####################################################################
## Creates a zip file from a given path of a lambda function. The  ##
## created file can directly be upload to AWS Lambda.              ##
#####################################################################


if [[ $# -eq 0 ]] ; then
    echo 'Error: No path provided'
    echo -e "\nUsage: $0 /path/to/lambda/fucntion \n" 
    exit 1
fi

folderName=$(basename $1)

cd $1

mkdir -p ../tmp
cp * ../tmp
cd ../tmp
zip -r ../${folderName}.zip .
cd ..
rm -r tmp