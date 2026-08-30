output "distribution_id" {
  description = "CloudFront distribution ID"
  value       = aws_cloudfront_distribution.main.id
}

output "distribution_domain_name" {
  description = "CloudFront distribution domain name"
  value       = aws_cloudfront_distribution.main.domain_name
}

output "distribution_arn" {
  description = "CloudFront distribution ARN"
  value       = aws_cloudfront_distribution.main.arn
}

output "distribution_zone_id" {
  description = "CloudFront distribution Zone ID"
  value       = aws_cloudfront_distribution.main.hosted_zone_id
}

output "distribution_aliases" {
  description = "CloudFront distribution aliases"
  value       = aws_cloudfront_distribution.main.aliases
}