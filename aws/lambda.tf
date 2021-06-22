# Shared credentials file and region configuration

variable "region" {
  type        = string
  description = "The AWS region for the deployment. See https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.RegionsAndAvailabilityZones.html"
  default = "us-east-1"
}

provider "aws" {
  shared_credentials_file = "credentials"
  region                  = var.region
}

# Create a new aws iam role
resource "aws_iam_role" "iam_for_lambda" {
  name_prefix = "iam_for_lambda"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}



# Configuration of the lambda layers
resource "aws_lambda_layer_version" "textblob_layer" {
  filename   = "./layers/textblob-for-amazon-linux-env.zip"
  layer_name = "textblob_layer"
  
  compatible_runtimes = ["python3.7"]
}

resource "aws_lambda_layer_version" "tflite_layer" {
  filename   = "./layers/tflite-for-amazon-linux-env.zip"
  layer_name = "tflite_layer"
  
  compatible_runtimes = ["python3.7"]
}





# Configuration of the lambda functions

locals {
  function_names = ["sentim-batch","sentim-inference-textblob","sentim-inference","sentim-preprocess","sentim-reduce"]
  layers = [[],[aws_lambda_layer_version.textblob_layer.arn],[aws_lambda_layer_version.tflite_layer.arn],[],[]]
}




resource "aws_lambda_function" "lambda" {
  count = length(local.function_names)

  filename      = "tmp/${local.function_names[count.index]}.zip"
  function_name = local.function_names[count.index]
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "lambda_function.lambda_handler"
  timeout       = 60
  memory_size   =  128
  runtime = "python3.7"
  layers = local.layers[count.index]
  source_code_hash = filebase64sha256( "tmp/${local.function_names[count.index]}.zip")
}


############################################
# Gateway sentim-inference-textblob_new    #
############################################

resource "aws_api_gateway_rest_api" "example" {
  count = length(local.function_names)

  name        = "ServerlessExample"
  description = "Terraform Serverless Application Example"
}

resource "aws_api_gateway_resource" "proxy" {
   count = length(local.function_names)
   
   rest_api_id = aws_api_gateway_rest_api.example[count.index].id
   parent_id   = aws_api_gateway_rest_api.example[count.index].root_resource_id
   path_part   = "{proxy+}"
}

resource "aws_api_gateway_method" "proxy" {
   count = length(local.function_names)


   rest_api_id   = aws_api_gateway_rest_api.example[count.index].id
   resource_id   = aws_api_gateway_resource.proxy[count.index].id
   http_method   = "ANY"
   authorization = "NONE"
}

resource "aws_api_gateway_integration" "lambda" {
   count = length(local.function_names)

   rest_api_id = aws_api_gateway_rest_api.example[count.index].id
   resource_id = aws_api_gateway_method.proxy[count.index].resource_id
   http_method = aws_api_gateway_method.proxy[count.index].http_method

   integration_http_method = "POST"
   type                    = "AWS_PROXY"
   uri                     = aws_lambda_function.lambda[count.index].invoke_arn
}

resource "aws_api_gateway_method" "proxy_root" {
   count = length(local.function_names)

   rest_api_id   = aws_api_gateway_rest_api.example[count.index].id
   resource_id   = aws_api_gateway_rest_api.example[count.index].root_resource_id
   http_method   = "ANY"
   authorization = "NONE"
}

resource "aws_api_gateway_integration" "lambda_root" {
   count = length(local.function_names)

   rest_api_id = aws_api_gateway_rest_api.example[count.index].id
   resource_id = aws_api_gateway_method.proxy_root[count.index].resource_id
   http_method = aws_api_gateway_method.proxy_root[count.index].http_method

   integration_http_method = "POST"
   type                    = "AWS_PROXY"
   uri                     = aws_lambda_function.lambda[count.index].invoke_arn
}

resource "aws_api_gateway_deployment" "example0" {
   depends_on = [
     aws_api_gateway_integration.lambda[0],
     aws_api_gateway_integration.lambda_root[0],
   ]

   rest_api_id = aws_api_gateway_rest_api.example[0].id
   stage_name  = local.function_names[0]
}

resource "aws_api_gateway_deployment" "example1" {
   depends_on = [
     aws_api_gateway_integration.lambda[1],
     aws_api_gateway_integration.lambda_root[1],
   ]

   rest_api_id = aws_api_gateway_rest_api.example[1].id
   stage_name  = local.function_names[1]
}

resource "aws_api_gateway_deployment" "example2" {
   depends_on = [
     aws_api_gateway_integration.lambda[2],
     aws_api_gateway_integration.lambda_root[2],
   ]

   rest_api_id = aws_api_gateway_rest_api.example[2].id
   stage_name  = local.function_names[2]
}

resource "aws_api_gateway_deployment" "example3" {
   depends_on = [
     aws_api_gateway_integration.lambda[3],
     aws_api_gateway_integration.lambda_root[3],
   ]

   rest_api_id = aws_api_gateway_rest_api.example[3].id
   stage_name  = local.function_names[3]
}

resource "aws_api_gateway_deployment" "example4" {
   depends_on = [
     aws_api_gateway_integration.lambda[4],
     aws_api_gateway_integration.lambda_root[4],
   ]

   rest_api_id = aws_api_gateway_rest_api.example[4].id
   stage_name  = local.function_names[4]
}

resource "aws_lambda_permission" "apigw" {
   count = length(local.function_names)

   statement_id  = "AllowAPIGatewayInvoke"
   action        = "lambda:InvokeFunction"
   function_name = aws_lambda_function.lambda[count.index].function_name
   principal     = "apigateway.amazonaws.com"

   # The "/*/*" portion grants access from any method on any resource
   # within the API Gateway REST API.
   source_arn = "${aws_api_gateway_rest_api.example[count.index].execution_arn}/*/*"
}



output "url_sentim-batch" {
  value = aws_api_gateway_deployment.example0.invoke_url
}
output "url_sentim-inference-textblob" {
  value = aws_api_gateway_deployment.example1.invoke_url
}
output "url_sentim-inference" {
  value = aws_api_gateway_deployment.example2.invoke_url
}
output "url_sentim-preprocess" {
  value = aws_api_gateway_deployment.example3.invoke_url
}
output "url_sentim-reduce" {
  value = aws_api_gateway_deployment.example4.invoke_url
}
