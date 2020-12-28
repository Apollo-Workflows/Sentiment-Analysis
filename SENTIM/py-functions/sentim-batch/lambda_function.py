import math

# https://stackoverflow.com/a/1751478
def batch(arr, n):
    n = max(1, n)
    return list((arr[i:i+n] for i in range(0, len(arr), n)))

def lambda_handler(event, context): 
  all_tweets = event['all_tweets']
  num_batches = event['num_batches']
  batch_size = math.ceil(len(all_tweets) / num_batches)
  
  batched_all_tweets = batch(all_tweets, batch_size)

  keyed = [ { 'tweets': batch } for batch in batched_all_tweets ]
  
  batches = { 'batches': keyed }
  return batches
  

