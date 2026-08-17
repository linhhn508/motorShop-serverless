output "products_table_name" { value = aws_dynamodb_table.products.name }
output "feedback_table_name" { value = aws_dynamodb_table.feedback.name }
output "contacts_table_name" { value = aws_dynamodb_table.contacts.name }
output "products_table_arn" { value = aws_dynamodb_table.products.arn }
output "feedback_table_arn" { value = aws_dynamodb_table.feedback.arn }
output "contacts_table_arn" { value = aws_dynamodb_table.contacts.arn }
