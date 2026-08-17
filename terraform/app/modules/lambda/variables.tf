variable "project_name" {
  type = string
}
variable "lambda_exec_role_arn" {
  type = string
}
variable "lambda_package_path" {
  type    = string
  default = "../backend/package.zip"
}
variable "products_table_name" {
  type = string
}
variable "feedback_table_name" {
  type = string
}
variable "contacts_table_name" {
  type = string
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