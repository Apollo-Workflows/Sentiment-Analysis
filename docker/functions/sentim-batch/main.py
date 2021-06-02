import json
import math

def batch(arr, n):
    n = max(1, n)
    return list((arr[i:i+n] for i in range(0, len(arr), n)))


def main(j):
  all_tweets = j['arrayToSplit']
  desired_num_batches = j['splitNumber']
  
  # do the calculation
  batch_size = math.ceil(len(all_tweets) / desired_num_batches)
  batched_all_tweets = batch(all_tweets, batch_size)
  keyed = [ { 'tweets': batch } for batch in batched_all_tweets ]
  
  # return the result
  res = { 
    'subArrays': keyed, 
    'num_batches': len(batched_all_tweets), 
    'num_tweets_total': len(all_tweets)
  }

  return res

if __name__ == "__main__":

  import sys
  import json

  # read the json
  f = open("jsonInput.json")
  j = json.loads(f.read())

  result = main(j)
  # write to std out
  print (json.dumps(result))