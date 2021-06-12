#!/bin/bash
#####################################################################
## Creates a zip file from a given path of a ibm function. The     ##
## created file can directly be upload to IBM Cloud.               ##
#####################################################################


if [[ $# -eq 0 ]] ; then
    echo 'Error: No path provided'
    echo -e "\nUsage: $0 /path/to/lambda/fucntion \n" 
    exit 1
fi

folderName=$(basename $1)
pwd=$(pwd)

cd $1

mkdir -p ../tmp
cp -r * ../tmp
cd ../tmp
mv main.py __main__.py
rm Dockerfile
zip -r $pwd/tmp/${folderName}.zip .
cd ..
rm -r tmp