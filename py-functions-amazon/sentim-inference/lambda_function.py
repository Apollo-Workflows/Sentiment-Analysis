import sys
import re
import os
import random
# Python 3.7
# Uses this TF Lite Layer: https://jak-sentim-bucket.s3.eu-central-1.amazonaws.com/tflite-for-amazon-linux-env.zip

sys.path.append('/opt/site-packages')  # make Python see TF Lite Layer

import numpy as np
import tflite_runtime.interpreter as tflite
# Reserved values in ImdbDataSet dic:
#  0      used for padding
#  1    mark for the start of a sentence
#  2  mark for unknown words (OOV)
IMDB_PAD = 0
IMDB_START = 1
IMDB_UNKNOWN = 2

# load model
interpreter = tflite.Interpreter(
    model_path="/var/task/text_classification_v2.tflite")
interpreter.allocate_tensors()

# get input and  output tensors
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()


# Converts an array of words ("tokens") to the int32 representation used in the NN
def toImdbVocab(tokens):
    # TODO solve seg fault on nubers > 16000 (something with int32? maybe np throws?)
    with open('/var/task/imdb-head.vocab') as vocabf:
        lines = [l.replace('\n', '') for l in vocabf.readlines()]
        translatedTokens = []
        # Prepend IMDB_START
        translatedTokens.append(IMDB_START)
        # translated each token to interger according to imdb.vocav
        for token in tokens:
            translatedToken = IMDB_UNKNOWN
            try:
                translatedToken = lines.index(token)+1  # TODO +1 or not?
                # ensure we don't tap into reserved values
                if (translatedToken is IMDB_PAD or translatedToken is IMDB_START):
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
    print(asImdbvocab)
    input_data = toNetInput(asImdbvocab)
    print(input_data)
    interpreter.set_tensor(input_details[0]['index'], input_data)
    # invoke NN
    interpreter.invoke()
    # collect sentiment
    output_data = interpreter.get_tensor(output_details[0]['index'])[0]

    #  retry 3 times
    if((type(output_data[0]) is not np.float32) or (type(output_data[1]) is not np.float32)):
      return [None, None] #zero confidence in either measurement
    else: 
    #  [ POS_CONF, NEG_CONF ]
      return [float(output_data[0]), float(output_data[1])]


def isNumber(sth):
    return (type(sth) is int) or (type(sth) is float)  # sufficient for us


def annotate_sentim_tweet(tweet):
    sentences = tweet['sentences']
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

    if((poslen > 0) and (neglen > 0)):
        tweet_sentiment = [possum / poslen, negsum / neglen]  # mean avg

    res = {**tweet, 'sentiment': tweet_sentiment}
    # reduce size of output, we can identify tweets later by their tweet_id
    res.pop('sentences', None)

    return res

################################

# Gets array of { sentences: string[], id: number, location: string}
# Uses pre-trained IMDB model to infer sentiment per sentence
# Returns array of { sentences: string[], id: number, location: string, sentiment: [ number, number ]}


def lambda_handler(event, context):
    tokenized_tweets = event['tokenized_tweets']
    resArr = []

    # Tweets, each annotated with "sentiment: [ POS_CONFIDENCE, NEG_CONFIDENCE ]" (between 0 and 1)
    annotated_tweets = [annotate_sentim_tweet(
        tweet) for tweet in tokenized_tweets]
    return {'annotated_tweets': annotated_tweets}
