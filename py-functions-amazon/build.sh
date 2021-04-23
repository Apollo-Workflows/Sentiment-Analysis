#!/bin/bash

if [[ $# -eq 0 ]] ; then
    echo 'Error: Please provide path do function'
    exit 1
fi

folderName=$(basename $1)

echo $folderName

cd $1

mkdir -p ../tmp
cp * ../tmp
cd ../tmp
rm lambda_function.py
mv lambda_function_apollo.py lambda_function.py
zip -r ../${folderName}.zip .
cd ..
rm -r tmp