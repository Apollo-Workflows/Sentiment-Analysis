#!/bin/bash

rm lambda-functions/*.zip

./build.sh lambda-functions/sentim-batch
./build.sh lambda-functions/sentim-inference
./build.sh lambda-functions/sentim-inference-textblob
./build.sh lambda-functions/sentim-preprocess
./build.sh lambda-functions/sentim-reduce

terraform init

terraform apply -auto-approve

rm lambda-functions/*.zip