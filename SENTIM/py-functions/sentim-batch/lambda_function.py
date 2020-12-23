# https://stackoverflow.com/a/1751478
def batch(arr, n):
    n = max(1, n)
    return list((arr[i:i+n] for i in range(0, len(arr), n)))

def lambda_handler(event, context): 
  all_tweets = event['all_tweets']
  batch_size = event['batch_size'] # number of tweets per batch

  batched_all_tweets = batch(all_tweets, batch_size)

  return batched_all_tweets
  

