resource "aws_dynamodb_table" "products" {
  name         = "${var.project_name}-products"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"

  attribute {
    name = "id"
    type = "S"
  }

  attribute {
    name = "category"
    type = "S"
  }

  global_secondary_index {
    name = "category-index"
    key_schema {
      attribute_name = "category"
      key_type       = "HASH"
    }
    projection_type = "ALL"
  }
}

resource "terraform_data" "dynamodb_script_seed" {
  triggers_replace = {
    file_hash = filesha256("${path.module}/assets/seed_data.json")
  }

  provisioner "local-exec" {
    command = "python3 ${path.module}/assets/seed_job.py ${aws_dynamodb_table.products.name} ${path.module}/assets/seed_data.json"
  }

  depends_on = [aws_dynamodb_table.products]
}
