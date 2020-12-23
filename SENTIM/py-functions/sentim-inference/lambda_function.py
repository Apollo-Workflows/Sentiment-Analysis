import sys

# Uses this TF Lite Layer: https://jak-sentim-bucket.s3.eu-central-1.amazonaws.com/tflite-for-amazon-linux-env.zip

def lambda_handler(event, context): 
  sys.path.append('/opt/site-packages') # make Python see it
  import tflite_runtime.interpreter as tflite
  print("tflite imported")