import json

from .main import sentim_batch

# Wrapper for OpenFaaS
def handle(event):
  req_json = json.loads(event)

  return sentim_batch(req_json), 200
