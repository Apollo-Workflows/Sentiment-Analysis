import json
import math 

def handler(request_json): 

  request = request_json.get_json()

  InferenceOutputs = request['InferenceOutputs'] # AFCL-generated collection
  grouped = {}

  # Group tweets over all batches by location
  for annotated_tweets in InferenceOutputs:
    for annotated_tweet in annotated_tweets:
    #  print("tweet:", annotated_tweet)
      location = annotated_tweet['state_of_closest_capital']
      if((location in grouped) is False): 
        grouped[location] = []
        # TODO stip everything but sentiment
        # or reduce compleetely per state, add stdderivation, mean, percentiles etc
      grouped[location].append(annotated_tweet)

  # Calculate metrics over all batches
  metrics = { 'average_sentiment': { } }
  churns = []
  for (location, location_tweets) in grouped.items():
    sentiments = [ tweet['sentiment'] for tweet in location_tweets ]
  
    valid_sentiments = [ s for s in sentiments if (isinstance(s[0], float) and isinstance(s[1], float))]

    # Note churn 
    churn = (len(sentiments) - len(valid_sentiments)) / len(sentiments)
    churns.append(churn)

   
    slice0 = [el[0] for el in valid_sentiments ]
    slice1 = [el[1] for el in valid_sentiments ]

    avg0 = None
    avg1 = None 
    if(len(slice0) > 0): # beware of division by zero
      avg0 = sum(slice0) / len(slice0)
    if(len(slice0) > 0):
      avg1 = sum(slice1) / len(slice1)

    metrics['average_sentiment'][location] = [ avg0, avg1 ]
    
  # Compute average churn 
  churn = None 
  if(len(churns) > 0):
    churn = sum(churns) / len(churns)
  # We cannot know at compile time what fields (eg. locations such as 'NY' or 'LA) this function will return
  # To be compatible with AFCL, stringify the analysis
  # Alternative: stash it as report to S3 or similar
  analysis_json = json.dumps(metrics)
  res = { 
    'analysis_json': analysis_json,
    'churn': churn
  }

  return res