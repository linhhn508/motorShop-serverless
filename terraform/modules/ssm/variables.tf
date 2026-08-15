variable "project_name" {
  default = "serverless-motorShop"
  type    = string
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
