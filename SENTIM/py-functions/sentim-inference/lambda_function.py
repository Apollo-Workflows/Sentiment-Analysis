import sys

def lambda_handler(event, context): 
  sys.path.append('/opt') # make Python see it
  import tflite_runtime.interpreter as tflite
  print("tflite imported")