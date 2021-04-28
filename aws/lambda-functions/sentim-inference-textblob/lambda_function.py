import sys
import re
import os
import random
import json

sys.path.append('/opt/site-packages')  # make Python see Textblob layer

from textblob import TextBlob


def get_sentence_sentiment(sentence, ttl=3):

    print("sentence: ", " ".join(sentence))
    textbl = TextBlob(" ".join(sentence))
    # -1.0 to 1.0
    sentiment = textbl.sentiment.polarity
        # to form pos_conf, neg_conf (TODO)
    sent =  [ sentiment, -sentiment  ]
    print("get_sentence_sentiment res", sent)
    return sent


def annotate_sentim_tweet(tweet):
    sentences = tweet['sentences']
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
    json_input = json.loads(event['body'])
    
    tokenized_tweets = json_input['tokenized_tweets']
    resArr = []

    # Tweets, each annotated with "sentiment: [ POS_CONFIDENCE, NEG_CONFIDENCE ]" (between 0 and 1)
    annotated_tweets = [annotate_sentim_tweet(
        tweet) for tweet in tokenized_tweets]
    
    return {
        'statusCode': 200,
        'body': json.dumps({'annotated_tweets': annotated_tweets})
    }