import sys
import re
import os
import random
import json
import numpy as np
import tflite_runtime.interpreter as tflite


##################################################
########## Boilerplate wrapping code #############
##################################################

# IBM wrapper
def main(args):
    res = sentim_inference(args)
    return res


# AWS wrapper
def lambda_handler(event, context):
    # read in the args from the POST object
    json_input = json.loads(event["body"])
    res = sentim_inference(json_input)
    return {"statusCode": 200, "body": json.dumps(res)}


##################################################
##################################################
# Reserved values in ImdbDataSet dic:
#  0      used for padding
#  1    mark for the start of a sentence
#  2  mark for unknown words (OOV)
IMDB_PAD = 0
IMDB_START = 1
IMDB_UNKNOWN = 2

# load model
interpreter = tflite.Interpreter(model_path="text_classification_v2.tflite")
interpreter.allocate_tensors()

# get input and  output tensors
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()


# Converts an array of words ("tokens") to the int32 representation used in the NN
def toImdbVocab(tokens):
    # TODO solve seg fault on nubers > 16000 (something with int32? maybe np throws?)
    with open("imdb-head.vocab") as vocabf:
        lines = [l.replace("\n", "") for l in vocabf.readlines()]
        translatedTokens = []
        # Prepend IMDB_START
        translatedTokens.append(IMDB_START)
        # translated each token to interger according to imdb.vocav
        for token in tokens:
            translatedToken = IMDB_UNKNOWN
            try:
                translatedToken = lines.index(token) + 1  # TODO +1 or not?
                # ensure we don't tap into reserved values
                if translatedToken is IMDB_PAD or translatedToken is IMDB_START:
                    translatedToken = IMDB_UNKNOWN
            except:
                pass
            translatedTokens.append(translatedToken)
        return np.array(translatedTokens, dtype=np.int32)


# (3) Pad with zeroes to length 256


def toNetInput(imdbVocab):
    ret = np.zeros((1, 256), dtype=np.int32)
    for (idx, num) in enumerate(imdbVocab):
        ret[0][idx] = num
    return ret


# TODO catch when unsuccessful, note churn

# This isn't deterministic between runs...


def get_sentence_sentiment(sentence, ttl=3):

    # return [random.random(), random.random()]
    # prepare sentence
    asImdbvocab = toImdbVocab(sentence)
    input_data = toNetInput(asImdbvocab)
    interpreter.set_tensor(input_details[0]["index"], input_data)
    # invoke NN
    interpreter.invoke()
    # collect sentiment
    output_data = interpreter.get_tensor(output_details[0]["index"])[0]

    #  retry 3 times
    if (type(output_data[0]) is not np.float32) or (
        type(output_data[1]) is not np.float32
    ):
        return [None, None]  # zero confidence in either measurement
    else:
        #  [ POS_CONF, NEG_CONF ]
        return [float(output_data[0]), float(output_data[1])]


def isNumber(sth):
    return (type(sth) is int) or (type(sth) is float)  # sufficient for us


def annotate_sentim_tweet(tweet):
    sentences = tweet["sentences"]
    sentence_sentiments = []
    for sentence in sentences:
        sentence_sentiment = get_sentence_sentiment(sentence, ttl=3)
        sentence_sentiments.append(sentence_sentiment)
    # Mean-average positive and negative confidence of per-sentence sentiment over the whole tweet

    possum = sum([ss[0] for ss in sentence_sentiments if ss[0]])
    poslen = len([ss[0] for ss in sentence_sentiments if ss[0]])

    negsum = sum([ss[1] for ss in sentence_sentiments if ss[1]])
    neglen = len([ss[1] for ss in sentence_sentiments if ss[1]])

    tweet_sentiment = [None, None]

    if (poslen > 0) and (neglen > 0):
        tweet_sentiment = [possum / poslen, negsum / neglen]  # mean avg

    if tweet_sentiment[0] != tweet_sentiment[0]:
        tweet_sentiment[0] = None

    if tweet_sentiment[1] != tweet_sentiment[1]:
        tweet_sentiment[1] = None

    res = {**tweet, "sentiment": tweet_sentiment}
    # reduce size of output, we can identify tweets later by their tweet_id
    res.pop("sentences", None)

    return res


# Gets array of { sentences: string[], id: number, location: string}
# Uses pre-trained IMDB model to infer sentiment per sentence
# Returns array of { sentences: string[], id: number, location: string, sentiment: [ number, number ]}


def sentim_inference(j):

    tokenized_tweets = j["tokenized_tweets"]
    resArr = []

    # Tweets, each annotated with "sentiment: [ POS_CONFIDENCE, NEG_CONFIDENCE ]" (between 0 and 1)
    annotated_tweets = [annotate_sentim_tweet(tweet) for tweet in tokenized_tweets]

    return {"annotated_tweets": annotated_tweets}


# Docker wrapper
if __name__ == "__main__":
    # read the json
    json_input = json.loads(open("jsonInput.json").read())
    result = sentim_inference(json_input)

    # write to std out
    print(json.dumps(result))