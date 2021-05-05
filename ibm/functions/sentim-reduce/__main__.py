import json
import math 

def main(args):
  InferenceOutputs = args['InferenceOutputs'] # AFCL-generated collection
  
  # flatten
  all_tweets = []
  for annotated_tweets in InferenceOutputs:
    for annotated_tweet in annotated_tweets:
      all_tweets.append(annotated_tweet)
      

  # filter invalid tweets
  valid_tweets = [ t for t in all_tweets if ((type(t['sentiment'][0]) is float) and (type(t['sentiment'][1]) is float)) ]

  # group by state_of_closest_capital
  grouped = {}
  


  # Group tweets over all batches by location
    #  print("tweet:", annotated_tweet)
  for tweet in valid_tweets:
    location = tweet['state_of_closest_capital']
    if((location in grouped) is False): 
      grouped[location] = []
      # TODO stip everything but sentiment
      # or reduce compleetely per state, add stdderivation, mean, percentiles etc
    grouped[location].append(tweet)

  ##################################################
  # Calculate churn
  
  churn = (len(all_tweets) - len(valid_tweets)) / len(all_tweets)

  ##################################################

  metrics = { 'average_sentiment': { } }

  ##################################################
  # Calculate average_sentiment per location
  for (location, location_tweets) in grouped.items():
    sentiments = [ tweet['sentiment'] for tweet in location_tweets ]
  
    valid_sentiments = [ s for s in sentiments if ((s[0] is not None) and (s[1] is not None))]
   
    slice0 = [el[0] for el in valid_sentiments ]
    slice1 = [el[1] for el in valid_sentiments ]

    avg0 = None
    avg1 = None 
    if(len(slice0) > 0): # beware of division by zero
      avg0 = sum(slice0) / len(slice0)
    if(len(slice1) > 0):
      avg1 = sum(slice1) / len(slice1)

    metrics['average_sentiment'][location] = [ avg0, avg1 ]
  ##################################################
    
  
  # We cannot know at compile time what fields (eg. locations such as 'NY' or 'LA) this function will return
  # To be compatible with AFCL, stringify the analysis
  # Alternative: stash it as report to S3 or similar
  res = { 
    'analysis_json': metrics,
    'churn': churn
  }
  
  return res