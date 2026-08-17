output "api_endpoint" { value = aws_api_gateway_stage.prod.invoke_url }
output "stage_name" { value = aws_api_gateway_stage.prod.stage_name }
output "execution_arn" { value = aws_api_gateway_rest_api.api.execution_arn }
