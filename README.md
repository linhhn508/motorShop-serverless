# motorShop Serverless

motorShop app deployed with AWS Lambda + API Gateway + DynamoDB + S3 + CloudFront.

## Architecture
Browser → CloudFront → [S3 (SPA), S3 (images), API Gateway → Lambda → DynamoDB]

## Local dev
cd backend && uv sync && uv run pytest tests/ -v

## Deploy
terraform -chdir=infra/terraform apply