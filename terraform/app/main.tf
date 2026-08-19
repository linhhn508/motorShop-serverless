module "ssm" {
  source         = "./modules/ssm"
  project_name   = var.project_name
  jwt_secret     = var.jwt_secret
  admin_username = var.admin_username
  admin_password = var.admin_password
}

module "dynamodb" {
  source       = "./modules/dynamodb"
  project_name = var.project_name
}

module "iam" {
  source       = "./modules/iam"
  project_name = var.project_name
  dynamodb_table_arns = [
    module.dynamodb.products_table_arn,
  ]
  ssm_parameter_arns = [
    module.ssm.admin_password_arn,
    module.ssm.admin_username_arn,
    module.ssm.jwt_secret_arn
  ]
}

module "lambda" {
  source               = "./modules/lambda"
  project_name         = var.project_name
  lambda_exec_role_arn = module.iam.lambda_exec_role_arn
  products_table_name  = module.dynamodb.products_table_name
  jwt_secret           = var.jwt_secret
  admin_username       = var.admin_username
  admin_password       = var.admin_password
  lambda_package_path  = var.lambda_package_path
}

module "apigateway" {
  source               = "./modules/apigateway"
  project_name         = var.project_name
  lambda_invoke_arn    = module.lambda.invoke_arn
  lambda_function_name = module.lambda.function_name
}

data "aws_s3_bucket" "project" {
  bucket = var.project_bucket
}

locals {
  # Strips the "https://" prefix and trailing slashes from the API endpoint
  api_domain = regex("^https?://([^/]+)", module.apigateway.api_endpoint)[0]
}


module "cloudfront" {
  source                              = "./modules/cloudfront"
  project_name                        = var.project_name
  environment                         = var.environment
  project_bucket_id                   = data.aws_s3_bucket.project.id
  project_bucket_arn                  = data.aws_s3_bucket.project.arn
  project_bucket_regional_domain_name = data.aws_s3_bucket.project.bucket_regional_domain_name
  apigateway_url                      = local.api_domain
  apigateway_stage_name               = module.apigateway.stage_name
}