# Access variable from terraform.tfvars
variable "ibmcloud_api_key" {}

# Support ibm provider
terraform {
  required_providers {
    ibm = {
      source  = "IBM-Cloud/ibm"
      version = "~> 1.23.2"
    }
  }
}

variable "region" {
  type        = string
  description = "The AWS region for the deployment. See https://cloud.ibm.com/docs/containers?topic=containers-regions-and-zones"
  default = "eu-de"
}

# Credentials and region configuration
provider "ibm" {
  ibmcloud_api_key   = var.ibmcloud_api_key
  region             = var.region
  alias              = "region"
}


locals {
  function_names = ["sentim-batch","sentim-inference-textblob","sentim-inference","sentim-preprocess","sentim-reduce"]
}



# Function configuration
resource "ibm_function_action" "functions" {
  count = length(local.function_names)

  name      = local.function_names[count.index]
  namespace = "apollo"
  provider = ibm.region

  exec {
    kind = "python:3.7"
    code_path = "functions/${local.function_names[count.index]}.zip"
  }

  # Timeout and memory
  limits {
    timeout = "60000"
    memory  = "128"
  }

  user_defined_annotations = <<EOF
        [
    {
        "key":"web-export",
        "value":true
    }
]
EOF


}



output "url_sentim-batch" {
  value = "${ibm_function_action.functions[0].target_endpoint_url}.json"
}

output "url_sentim-inference-textblob" {
  value = "${ibm_function_action.functions[1].target_endpoint_url}.json"
}

output "url_sentim-inference" {
  value = "${ibm_function_action.functions[2].target_endpoint_url}.json"
}

output "url_sentim-preprocess" {
  value = "${ibm_function_action.functions[3].target_endpoint_url}.json"
}

output "url_sentim-reduce" {
  value = "${ibm_function_action.functions[4].target_endpoint_url}.json"
}