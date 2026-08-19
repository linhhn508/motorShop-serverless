variable "project_name" {
  type = string
}
variable "lambda_exec_role_arn" {
  type = string
}
variable "lambda_package_path" {
  type = string
}
variable "products_table_name" {
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