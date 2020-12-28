
# TODO put together ie undo batching

# Group tweets by location
def lambda_handler(event, context): 
  annotated_tweets = event['annotated_tweets']
  grouped = {}

  for annotated_tweet in annotated_tweets:
    location = annotated_tweet['location']
    if((location in grouped) is False): 
      grouped[location] = []
      # TODO stip everything but sentiment
      # or reduce compleetely per state, add stdderivation, mean, percentiles etc
    grouped[location].append(annotated_tweet)


  metrics = { 'average_sentiment': { } }
  for (location, location_tweets) in grouped.items():
    sentiments = [ tweet['sentiment'] for tweet in location_tweets ]
    slice0 = [el[0] for el in sentiments ]
    slice1 = [el[1] for el in sentiments ]

    avg0 = sum(slice0) / len(slice0)
    avg1 = sum(slice1) / len(slice1)

    metrics['average_sentiment'][location] = [ avg0, avg1 ]

  return metrics
