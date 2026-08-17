variable "project_name" { type = string }
variable "dynamodb_table_arns" { type = list(string) }
variable "ssm_parameter_arns" { type = list(string) }