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
    module.dynamodb.feedback_table_arn,
    module.dynamodb.contacts_table_arn
  ]
  ssm_parameter_arns = [
    module.ssm.admin_password_arn,
    module.ssm.admin_username_arn,
    module.ssm.jwt_secret_arn
  ]
}

module "s3" {
  source       = "./modules/s3"
  project_name = var.project_name
  bucket_names = ["images", "frontend"]
}


module "lambda" {
  source               = "./modules/lambda"
  project_name         = var.project_name
  lambda_exec_role_arn = module.iam.lambda_exec_role_arn
  products_table_name  = module.dynamodb.products_table_name
  feedback_table_name  = module.dynamodb.feedback_table_name
  contacts_table_name  = module.dynamodb.contacts_table_name
  jwt_secret           = var.jwt_secret
  admin_username       = var.admin_username
  admin_password       = var.admin_password
}

module "apigateway" {
  source               = "./modules/apigateway"
  project_name         = var.project_name
  lambda_invoke_arn    = module.lambda.invoke_arn
  lambda_function_name = module.lambda.function_name
}

data "aws_s3_bucket" "images" {
  bucket = module.s3.project_bucket_names["images"]
}

data "aws_s3_bucket" "frontend" {
  bucket = module.s3.project_bucket_names["frontend"]
}

locals {
  # Strips the "https://" prefix and trailing slashes from the API endpoint
  api_domain = regex("^https?://([^/]+)", module.apigateway.api_endpoint)[0]
}


module "cloudfront" {
  source                               = "./modules/cloudfront"
  project_name                         = var.project_name
  environment                          = var.environment
  frontend_bucket_id                   = data.aws_s3_bucket.frontend.id
  frontend_bucket_arn                  = data.aws_s3_bucket.frontend.arn
  frontend_bucket_regional_domain_name = data.aws_s3_bucket.frontend.bucket_regional_domain_name
  images_bucket_id                     = data.aws_s3_bucket.images.id
  images_bucket_arn                    = data.aws_s3_bucket.images.arn
  images_bucket_regional_domain_name   = data.aws_s3_bucket.images.bucket_regional_domain_name
  apigateway_url                       = local.api_domain
  apigateway_stage_name                = module.apigateway.stage_name
}