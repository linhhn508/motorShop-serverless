output "project_bucket_names" {
  value = { for name, bucket in aws_s3_bucket.motorShop : name => bucket.id }
}