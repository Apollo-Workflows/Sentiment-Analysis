import re

def preprocess(tweet): 
  processed = tweet.split(" ") # split
  # replace weird chars
  processed = [ re.sub("[^0-9a-zA-Z]+", "", word) for word in processed ] 
  # filter empty strings
  processed = [ word for word in processed if word ]
  return processed 


def lambda_handler(event, context):
  print(event)
  tweets = event['tweets']
  preprocessed_tweets = [ preprocess(tweet) for tweet in tweets ]
  return { 
    'tokens': preprocessed_tweets
  }