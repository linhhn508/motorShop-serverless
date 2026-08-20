import json
import boto3
import sys

def seed_data(table_name, file_path):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    
    with open(file_path, 'r') as f:
        items = json.load(f)
        
    with table.batch_writer() as batch:
        for item in items:
            batch.put_item(Item=item)
    print(f"Successfully seeded {len(items)} items.")

if __name__ == "__main__":
    # Nhận tham số truyền vào từ Terraform
    seed_data(sys.argv[1], sys.argv[2])
