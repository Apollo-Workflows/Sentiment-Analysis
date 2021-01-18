import re

# { 'text': string, 'id': number, 'location': 'string' }
def preprocess(tweet): 
  # split text into sentences
  if(('text' in tweet) is False):
    return None 
  text = tweet['text']
  sentences = text.replace('!', '.').replace('?', '.').split('.') # quick and dirty
  # filter empty strings (sentences)
  sentences = [ sentence for sentence in sentences if sentence ]
  # In each sentence, only keep alpha numeric
  sencences = [ re.sub('[^0-9a-zA-Z]+', '*', sentence) for sentence in sentences ]

  print("sentences: ", sentences)
  processed_sentences = []
  for sentence in sentences: 
    processed_sentence = sentence.split(" ") # split per word
    # replace weird chars
    processed_sentence = [ re.sub("[^0-9a-zA-Z]+", "", word) for word in processed_sentence ] 
    # filter empty strings (words)
    processed_sentence = [ word for word in processed_sentence if word ]

    # to lowercase 
    processed_sentence = [ word.lower() for word in processed_sentence ]

    processed_sentences.append(processed_sentence)
  
  # Return sentences in place of text
  res = {
    **tweet,
    'sentences': processed_sentences, 
  }
  res.pop('text', None)

  return res


# Tokenizes and normalizes (TODO) tweets
def lambda_handler(event, context):
  tweets = event['tweets']['tweets'] #TODO
  tokenized_tweets = [ preprocess(tweet) for tweet in tweets ]
  # filter out invalids 
  tokenized_tweets = [ t for t in tokenized_tweets if t ]
  return { 
    'tokenized_tweets': tokenized_tweets
  }