terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Point the AWS provider at LocalStack (a local AWS emulator) instead of real AWS.
# This lets us run a genuine `terraform apply` with no cloud account or credentials.
provider "aws" {
  region                      = "us-east-1"
  access_key                  = "test"
  secret_key                  = "test"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true
  s3_use_path_style           = true

  endpoints {
    s3       = "http://localhost:4566"
    dynamodb = "http://localhost:4566"
  }
}

# S3 bucket to store trained model artifacts.
resource "aws_s3_bucket" "model_artifacts" {
  bucket = "mlops-model-artifacts"
}

# DynamoDB table to record predictions made by the model.
resource "aws_dynamodb_table" "predictions" {
  name         = "predictions"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"

  attribute {
    name = "id"
    type = "S"
  }
}

output "bucket_name" {
  value = aws_s3_bucket.model_artifacts.bucket
}

output "table_name" {
  value = aws_dynamodb_table.predictions.name
}
