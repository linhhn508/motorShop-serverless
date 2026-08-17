resource "aws_ssm_parameter" "jwt_secret" {
  name  = "/${var.project_name}/JWT_SECRET"
  type  = "SecureString"
  value = var.jwt_secret
}

resource "aws_ssm_parameter" "admin_username" {
  name  = "/${var.project_name}/ADMIN_USERNAME"
  type  = "SecureString"
  value = var.admin_username
}

resource "aws_ssm_parameter" "admin_password" {
  name  = "/${var.project_name}/ADMIN_PASSWORD"
  type  = "SecureString"
  value = var.admin_password
}