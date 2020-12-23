import re

def preprocess(tweet): 
  sentences = tweet.replace('!', '.').replace('?', '.').split('.') # quick and dirty
  # filter empty strings (sentences)
  sentences = [ sentence for sentence in sentences if sentence ]
  print("sentences: ", sentences)
  processed_sentences = []
  for sentence in sentences: 
    processed_sentence = sentence.split(" ") # split per word
    # replace weird chars
    processed_sentence = [ re.sub("[^0-9a-zA-Z]+", "", word) for word in processed_sentence ] 
    # filter empty strings (words)
    processed_sentence = [ word for word in processed_sentence if word ]
    processed_sentences.append(processed_sentence)
  
  return processed_sentences


# Tokenizes and normalizes (TODO) tweets
def lambda_handler(event, context):
  tweets = event['tweets']
  tokenized_tweets = [ preprocess(tweet) for tweet in tweets ]
  return { 
    'tokenized_tweets': tokenized_tweets
  }