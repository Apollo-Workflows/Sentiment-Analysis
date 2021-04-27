# Sentiment Analysis

This workflow analyzes a large amount of Tweets using a pre-trained Tensorflow Net, or alternatively using NLTK language corpus lookup, to determine sentiment per US state.

#### Overview

This repository contains a parallel sentiment analysis implementation, orchestrated with the Abstract Function Choreography Language and runnable on the [Apollo Engine](https://github.com/Apollo-Core)


![workflow diagram](./diagrams/workflow-slim.svg)

**Fig 1: workflow.yaml control and data flow**



#### Get the code

```
git clone https://github.com/Apollo-Workflows/Sentiment-Analysis
cd Sentiment-Analysis
```

#### Deploy the serverless functions

The serverless functions are in `py-functions-amazon` or `py-functions-google`. You can deploy a mix of them to Amazon and Google, but `sentim-inference` is only available for Amazon.

Furthermore, ensure that `sentim-inference` has Tensorflow Lite available (you can attach this Lambda Layer: `s3://jak-sentim-bucket/tflite-for-amazon-linux-env.zip`), and runs on Python 3.7.

For auto deployment on AWS you can put your credentials file to `py-functions-amazon/credentials` and execute `./deploy.sh` (terraform needs to be installed).

#### Run the workflow


Open `workflow.yaml`, and update the `resource` fields to the ARNs of your deployed Lambdas. You can find the ARNs in your [AWS Lambda Console](http://console.aws.amazon.com/lambda).

```yaml
 ...
 properties:
    - name: "resource"
      value: "arn:aws:lambda:XXXXXXXXXXXXXXXXXXXXXX:sentim-inference"
 ...
```

Then, you can run the workflow:

```
$ java -jar YOUR_PATH_TO_xAFCL.jar ./workflow.yaml ./input.json
```


#### References

**Twitter data set**: [Z. Cheng, J. Caverlee, and K. Lee. You Are Where You Tweet: A Content-Based Approach to Geo-locating Twitter Users. In Proceeding of the 19th ACM Conference on Information and Knowledge Management (CIKM), Toronto, Oct 2010](https://archive.org/details/twitter_cikm_2010) (Accessed Dec 14 2020)

**Tensorflow Text classification model (used in `sentim-inference`):** [Text classification | Tensorflow Lite](https://www.tensorflow.org/lite/models/text_classification/overview) (Accessed Dec 22 2020)

**Textblob Library & NLTK corpora (used in `sentim-inference-textblob`)**: [sloria/TextBlob | GitHub](https://github.com/sloria/textblob) (Accessed Dec 25 2020)
