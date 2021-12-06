import json

from .main import sentim_inference

# Wrapper for OpenFaaS
def handle(event):
  req_json = json.loads(event)

  return sentim_inference(req_json), 200
