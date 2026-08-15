data "aws_caller_identity" "current" {}

# --- Frontend Static Site Bucket ---
resource "aws_s3_bucket" "motorShop" {
  for_each = toset(var.bucket_names)
  bucket   = "${var.project_name}-${each.value}-${data.aws_caller_identity.current.account_id}"

  tags = {
    Name    = "${var.project_name}-${each.value}"
    Purpose = "${each.value} static files"
  }
}

resource "aws_s3_bucket_public_access_block" "motorShop" {
  for_each                = toset(var.bucket_names)
  bucket                  = aws_s3_bucket.motorShop[each.value].id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "motorShop" {
  for_each = toset(var.bucket_names)
  bucket   = aws_s3_bucket.motorShop[each.value].id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}