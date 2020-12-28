import sys
import re
import os

# Python 3.7
# Uses this TF Lite Layer: https://jak-sentim-bucket.s3.eu-central-1.amazonaws.com/tflite-for-amazon-linux-env.zip

sys.path.append('/opt/site-packages') # make Python see TF Lite Layer
import numpy as np 
import tflite_runtime.interpreter as tflite

# Reserved values in ImdbDataSet dic:
#  0      used for padding
#  1    mark for the start of a sentence
#  2  mark for unknown words (OOV)
IMDB_PAD = 0
IMDB_START  = 1
IMDB_UNKNOWN = 2

# load model
interpreter = tflite.Interpreter(model_path="/var/task/text_classification_v2.tflite")
interpreter.allocate_tensors()

# get input and  output tensors
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()


# Converts an array of words ("tokens") to the int32 representation used in the NN
def toImdbVocab(tokens):
  with open('/var/task/imdb.vocab') as vocabf:
    lines = [ l.replace('\n', '') for l in  vocabf.readlines() ]
    translatedTokens = []
    # Prepend IMDB_START
    translatedTokens.append(IMDB_START)
    # translated each token to interger according to imdb.vocav
    for token in tokens:
      translatedToken = IMDB_UNKNOWN
      try:
        translatedToken = lines.index(token)+1 # TODO +1 or not?
      except: 
        pass 
      translatedTokens.append(translatedToken)
    return np.array(translatedTokens, dtype=np.int32)

# (3)
def toNetInput(imdbVocab):
  ret = np.zeros((1,256), dtype=np.int32)
  for (idx, num) in enumerate(imdbVocab):
    ret[0][idx] = num
  return ret 


def annotateSentimTweet(tweet): 
  sentences = tweet['sentences']
  sentence_sentiments = []
  for sentence in sentences:
      
    # prepare sentence
    asImdbvocab = toImdbVocab(sentence)
    input_data = toNetInput(asImdbvocab)
    print(input_data)
    interpreter.set_tensor(input_details[0]['index'], input_data)
    # invoke NN
    interpreter.invoke()
    # collect sentiment
    output_data = interpreter.get_tensor(output_details[0]['index'])[0]
    sentence_sentiments.append(output_data.tolist())
  # Mean-average positive and negative confidence of per-sentence sentiment over the whole tweet
  slice0 = [ el[0] for el in sentence_sentiments ]
  slice1 = [ el[1] for el in sentence_sentiments ]
  # Positive and negative sentiment confidence score
  # Something like [ 0.3028472, 0.7683728 ] 
  tweet_sentiment = [ sum(slice0) / len(slice0), sum(slice1) / len(slice1) ]

  return { **tweet, 'sentiment': tweet_sentiment}

################################

# Gets array of { sentences: string[], id: number, location: string}
# Uses pre-trained IMDB model to infer sentiment per sentence
# Returns array of { sentences: string[], id: number, location: string, sentiment: [ number, number ]}

def lambda_handler(event, context): 
  tokenized_tweets = event['tokenized_tweets']
  resArr = []

  # Tweets, each annotated with "sentiment: [ POS_CONFIDENCE, NEG_CONFIDENCE ]" (between 0 and 1)
  annotated_tweets = [ annotateSentimTweet(tweet) for tweet in tokenized_tweets ]
  return { 'annotated_tweets': annotated_tweets }
