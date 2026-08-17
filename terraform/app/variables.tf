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

variable "admin_password" {
  type      = string
  sensitive = true
}

variable "project_bucket" {
  type = string
}

variable "alert_email" {
  type = string
}
