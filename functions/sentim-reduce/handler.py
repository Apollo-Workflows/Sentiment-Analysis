import json

from .main import sentim_reduce

# Wrapper for OpenFaaS
def handle(event):
  req_json = json.loads(event)

  return sentim_reduce(req_json), 200
