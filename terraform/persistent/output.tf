output "serverless_bucket_name" {
  value = aws_s3_bucket.this.id
}

output "serverless_bucket_arn" {
  value = aws_s3_bucket.this.arn
}

output "serverless_bucket_regional_domain_name" {
  value = aws_s3_bucket.this.bucket_regional_domain_name
}