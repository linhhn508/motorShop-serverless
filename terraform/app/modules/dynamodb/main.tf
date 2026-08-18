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
