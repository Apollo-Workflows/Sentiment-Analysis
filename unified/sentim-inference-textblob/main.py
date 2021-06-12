import sys
import json
import sys
import re
import os
import random
import json
from textblob import TextBlob

##################################################
########## Boilerplate wrapping code #############
##################################################

# IBM wrapper
def main(args):
    res = sentim_inference(args)
    return res


def lambda_handler(event, context):
    # read in the args from the POST object
    json_input = json.loads(event["body"])
    res = sentim_inference(json_input)
    return {"statusCode": 200, "body": json.dumps(res)}


# Docker wrapper
if __name__ == "__main__":
    # read the json
    json_input = json.loads(open("jsonInput.json").read())
    result = sentim_inference(json_input)

    # write to std out
    print(json.dumps(result))


##################################################
##################################################


def get_sentence_sentiment(sentence, ttl=3):
    textbl = TextBlob(" ".join(sentence))
    # -1.0 to 1.0
    sentiment = textbl.sentiment.polarity
    # to form pos_conf, neg_conf (TODO)
    sent = [sentiment, -sentiment]
    return sent


def annotate_sentim_tweet(tweet):
    sentences = tweet["sentences"]
    sentence_sentiments = []
    for sentence in sentences:
        sentence_sentiment = get_sentence_sentiment(sentence, ttl=3)
        sentence_sentiments.append(sentence_sentiment)
    # Mean-average positive and negative confidence of per-sentence sentiment over the whole tweet

    possum = sum([ss[0] for ss in sentence_sentiments])
    poslen = len([ss[0] for ss in sentence_sentiments])

    negsum = sum([ss[1] for ss in sentence_sentiments])
    neglen = len([ss[1] for ss in sentence_sentiments])

    tweet_sentiment = [None, None]

    if (poslen > 0) and (neglen > 0):
        tweet_sentiment = [possum / poslen, negsum / neglen]  # mean avg

    res = {**tweet, "sentiment": tweet_sentiment}
    # reduce size of output, we can identify tweets later by their tweet_id
    res.pop("sentences", None)

    return res


################################

# Gets array of { sentences: string[], id: number, location: string}
# Uses pre-trained IMDB model to infer sentiment per sentence
# Returns array of { sentences: string[], id: number, location: string, sentiment: [ number, number ]}


def sentim_inference(j):
    tokenized_tweets = j["tokenized_tweets"]
    resArr = []

    # Tweets, each annotated with "sentiment: [ POS_CONFIDENCE, NEG_CONFIDENCE ]" (between 0 and 1)
    annotated_tweets = [annotate_sentim_tweet(tweet) for tweet in tokenized_tweets]

    return {"annotated_tweets": annotated_tweets}
