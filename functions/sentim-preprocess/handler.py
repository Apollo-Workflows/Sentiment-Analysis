import json

from .main import sentim_preprocess

# Wrapper for OpenFaaS
def handle(event):
  req_json = json.loads(event)

  return sentim_preprocess(req_json), 200
