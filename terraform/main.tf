# Provider Configuration
provider "aws" {
  region = var.aws_region
}

# DynamoDB Table - Mock CRM
resource "aws_dynamodb_table" "customers" {
  name           = "Customers"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "PhoneNumber"

  attribute {
    name = "PhoneNumber"
    type = "S"
  }

  tags = {
    Project     = "Intelligent-IVR"
    Environment = "Portfolio"
  }
}

# IAM Role for Lambda
resource "aws_iam_role" "lambda_role" {
  name = "ivr_lambda_execution_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# IAM Policy for DynamoDB Access
resource "aws_iam_role_policy" "lambda_dynamodb_policy" {
  name = "lambda_dynamodb_access"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem",
          "dynamodb:Query"
        ]
        Effect   = "Allow"
        Resource = aws_dynamodb_table.customers.arn
      },
      {
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Effect   = "Allow"
        Resource = "arn:aws:logs:*:*:*"
      }
    ]
  })
}

# Lambda: Customer Lookup
resource "aws_lambda_function" "customer_lookup" {
  filename      = "customer-lookup.zip"
  function_name = "IVR-Customer-Lookup"
  role          = aws_iam_role.lambda_role.arn
  handler       = "index.lambda_handler"
  runtime       = "python3.9"

  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.customers.name
    }
  }
}

# Lambda: Routing Logic
resource "aws_lambda_function" "routing_logic" {
  filename      = "routing-logic.zip"
  function_name = "IVR-Routing-Logic"
  role          = aws_iam_role.lambda_role.arn
  handler       = "index.lambda_handler"
  runtime       = "python3.9"
}

# Outputs
output "dynamodb_table_name" {
  value = aws_dynamodb_table.customers.name
}

output "customer_lookup_arn" {
  value = aws_lambda_function.customer_lookup.arn
}

output "routing_logic_arn" {
  value = aws_lambda_function.routing_logic.arn
}
