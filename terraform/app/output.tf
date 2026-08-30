output "cloudfront_domain" {
  value = module.cloudfront.distribution_domain_name
}

output "api_endpoint" {
  value = module.apigateway.api_endpoint
}

output "web_domain_name" {
  value = "https://${var.web_domain_name}"
}