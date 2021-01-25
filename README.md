# Sentiment Analysis

Sentiment Analysis is a common natural language processing task.
This workflow analyzed a large amount of Tweets using a pre-trained Tensorflow Net, or alternatively using NLTK language corpus lookup, to determine sentiment per US state.

#### Overview

This repository contains a parallel sentiment analysis implementation, orchestrated with the Abstract Function Choreography Language and runnable on the [xAFCL Enactment Engine](https://github.com/sashkoristov/enactmentengine)

There are two workflows flavors, `workflow` and `workflow-slim`:
* `workflows` are runnable, and well-tested on the current version of xAFCL.
* `workflows-slim` are aspirational workflows where the dataflow is optimized to its theoretical limit, but are not tested on the current version of xAFCL.


![workflow-slim diagram](./diagrams/workflow-slim.svg)

**Fig 1: workflow-slim.yaml control and data flow**



#### Get the code

```
git clone https://github.com/Apollo-Workflows/Sentiment-Analysis
cd Sentiment-Analysis
```

#### Get an input dataset

name | fetch command 
----|----
[`input-200-tweets.json`](https://github.com/Apollo-Workflows/Sentiment-Analysis/blob/master/datasets/input-200-tweets.json) | `wget https://github.com/Apollo-Workflows/Sentiment-Analysis/blob/master/datasets/input-200-tweets.json -O input.json`
[`input-5000-tweets.json`](https://github.com/Apollo-Workflows/Sentiment-Analysis/blob/master/datasets/input-5000-tweets.json) | `wget https://github.com/Apollo-Workflows/Sentiment-Analysis/blob/master/datasets/input-5000-tweets.json -O input.json` 
[`input-10000-tweets.json`](https://github.com/Apollo-Workflows/Sentiment-Analysis/blob/master/datasets/input-10000-tweets.json) | `wget https://github.com/Apollo-Workflows/Sentiment-Analysis/blob/master/datasets/input-10000-tweets.json -O input.json` 
[`input-15000-tweets.json`](https://github.com/Apollo-Workflows/Sentiment-Analysis/blob/master/datasets/input-15000-tweets.json) | `wget https://github.com/Apollo-Workflows/Sentiment-Analysis/blob/master/datasets/input-15000-tweets.json -O input.json` 
[`input-20000-tweets.json`](https://github.com/Apollo-Workflows/Sentiment-Analysis/blob/master/datasets/input-20000-tweets.json) | `wget https://github.com/Apollo-Workflows/Sentiment-Analysis/blob/master/datasets/input-20000-tweets.json -O input.json` 

The original authors of the datasets are [Z. Cheng, J. Caverlee, and K. Lee. You Are Where You Tweet: A Content-Based Approach to Geo-locating Twitter Users. In Proceeding of the 19th ACM Conference on Information and Knowledge Management (CIKM), Toronto, Oct 2010](https://archive.org/details/twitter_cikm_2010)

Then, update `input.json` with the desired parallelism. The default is 2 and 200, respectively for the datasets. This yields a 100 tweets per 1 inference function ratio for both datasets.


```
{
  "desired_num_batches": 2, // <--
  "all_tweets": [
    {
      "text": "@jennimichelle yes ma'am. St. Brides, Powell, Caldwell.",
      "tweet_id": 9219243277,
      "user_id": 18604078,
      "state_of_closest_capital": "WI",
      "date": "2010-02-16 22:25:03"
    },
    ......
  ]
```

#### Deploy the serverless functions

The serverless functions are in `py-functions-amazon` or `py-functions-google`. You can deploy a mix of them to Amazon and Google, but `sentim-inference` is only available for Amazon.

Furthermore, ensure that `sentim-inference` has Tensorflow Lite available (you can attach this Lambda Layer: `s3://jak-sentim-bucket/tflite-for-amazon-linux-env.zip`), and runs on Python 3.7.

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


#### Preliminary Metrics

##### Neural net inference

Measurements were not done in a controlled test environment.
Use for personal reference only.

![Chart showing metrics of input-200-tweets.json](https://github.com/ApolloCEC/workflows/blob/master/SENTIM/metrics/input-200-tweets-metrics.png)
![Chart showing metrics of input-20000-tweets.json](https://github.com/ApolloCEC/workflows/blob/master/SENTIM/metrics/input-20000-tweets-metrics.png)


#### References

**Twitter data set**: [Z. Cheng, J. Caverlee, and K. Lee. You Are Where You Tweet: A Content-Based Approach to Geo-locating Twitter Users. In Proceeding of the 19th ACM Conference on Information and Knowledge Management (CIKM), Toronto, Oct 2010](https://archive.org/details/twitter_cikm_2010) (Accessed Dec 14 2020)

**Tensorflow Text classification model (used in `sentim-inference`):** [Text classification | Tensorflow Lite](https://www.tensorflow.org/lite/models/text_classification/overview) (Accessed Dec 22 2020)

**Textblob Library & NLTK corpora (used in `sentim-inference-textblob`)**: [sloria/TextBlob | GitHub](https://github.com/sloria/textblob) (Accessed Dec 25 2020)
