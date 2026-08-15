output "jwt_secret_arn" { value = aws_ssm_parameter.jwt_secret.arn }
output "admin_username_arn" { value = aws_ssm_parameter.admin_username.arn }
output "admin_password_arn" { value = aws_ssm_parameter.admin_password.arn }