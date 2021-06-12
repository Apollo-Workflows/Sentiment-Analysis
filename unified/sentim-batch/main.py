import json
import math


##################################################
########## Boilerplate wrapping code #############
##################################################

# IBM wrapper
def main(args):
    res = sentim_inference(args)
    return res


def lambda_handler(event, context):
    # read in the args from the POST object
    json_input = json.loads(event["body"])
    res = sentim_inference(json_input)
    return {"statusCode": 200, "body": json.dumps(res)}


# Docker wrapper
if __name__ == "__main__":
    # read the json
    json_input = json.loads(open("jsonInput.json").read())
    result = sentim_inference(json_input)

    # write to std out
    print(json.dumps(result))


##################################################
##################################################


def batch(arr, n):
    n = max(1, n)
    return list((arr[i : i + n] for i in range(0, len(arr), n)))


def sentim_batch(json_input):
    all_tweets = json_input["arrayToSplit"]
    desired_num_batches = json_input["splitNumber"]

    # do the calculation
    batch_size = math.ceil(len(all_tweets) / desired_num_batches)
    batched_all_tweets = batch(all_tweets, batch_size)
    keyed = [{"tweets": batch} for batch in batched_all_tweets]

    # return the result
    res = {
        "subArrays": keyed,
        "num_batches": len(batched_all_tweets),
        "num_tweets_total": len(all_tweets),
    }
    return res
