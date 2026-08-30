variable "aws_region" {
  default = "ap-southeast-1"
}

variable "project_name" {
  default = "motorshop-serverless"
}

variable "environment" {
  default = "prod"
}

variable "jwt_secret" {
  type      = string
  sensitive = true
}

variable "admin_username" {
  type = string
}

variable "lambda_package_path" {
  type    = string
  default = "../../backend/package.zip"
}

variable "admin_password" {
  type      = string
  sensitive = true
}

variable "delegation_set_id" {
  type      = string
  sensitive = true
}

variable "web_domain_name" {
  type = string
}

variable "project_bucket" {
  type = string
}

variable "alert_email" {
  type = string
}
