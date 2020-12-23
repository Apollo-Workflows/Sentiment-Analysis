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

################################


# Gets an array of sentences (array of array of tokens / words)
# Uses pre-trained IMDB model to infer sentiment per sentence
# Returns array of [positive_sentiment_confidence, negative_sentiment_confidence]

def lambda_handler(event, context): 
  tokenArr = event['tokens']
  resArr = []

  # load model
  interpreter = tflite.Interpreter(model_path="/var/task/text_classification_v2.tflite")
  interpreter.allocate_tensors()

  # get input and  output tensors
  input_details = interpreter.get_input_details()
  output_details = interpreter.get_output_details()

  print(input_details)
  print(output_details)

  output = []

  # For each sentence (array of tokens), get sentiment
  for tokens in tokenArr:
    # prepare sentence
    asImdbvocab = toImdbVocab(tokens)
    input_data = toNetInput(asImdbvocab)
    print(input_data)
    interpreter.set_tensor(input_details[0]['index'], input_data)
    # invoke NN
    interpreter.invoke()
    # collect sentiment
    output_data = interpreter.get_tensor(output_details[0]['index'])
    output.append(output_data.tolist())
  
  return output
