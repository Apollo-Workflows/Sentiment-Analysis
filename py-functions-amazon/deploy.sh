#!/bin/bash

rm *.zip

./build.sh sentim-batch
./build.sh sentim-inference
./build.sh sentim-inference-textblob
./build.sh sentim-preprocess
./build.sh sentim-reduce

terraform apply -auto-approve