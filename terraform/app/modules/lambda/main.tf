resource "aws_lambda_function" "api" {
  function_name = "${var.project_name}-api"
  role          = var.lambda_exec_role_arn
  handler       = "app.main.handler"
  runtime       = "python3.12"
  filename      = var.lambda_package_path
  timeout       = 30
  memory_size   = 512

  environment {
    variables = {
      PRODUCTS_TABLE = var.products_table_name
      JWT_SECRET     = var.jwt_secret
      ADMIN_USERNAME = var.admin_username
      ADMIN_PASSWORD = var.admin_password
    }
  }
}

resource "aws_cloudwatch_log_group" "lambda" {
  name              = "/aws/lambda/${aws_lambda_function.api.function_name}"
  retention_in_days = 7
}
