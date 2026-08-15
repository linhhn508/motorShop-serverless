import boto3
from moto import mock_aws


@mock_aws
def test_get_dynamodb_resource_returns_resource():
    import os
    os.environ["AWS_DEFAULT_REGION"] = "ap-southeast-1"
    from app.db import get_dynamodb_resource
    resource = get_dynamodb_resource()
    assert resource is not None


@mock_aws
def test_get_table_returns_table_object():
    import os
    os.environ["AWS_DEFAULT_REGION"] = "ap-southeast-1"
    boto3.resource("dynamodb", region_name="ap-southeast-1").create_table(
        TableName="products",
        KeySchema=[{"AttributeName": "productId", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "productId", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST",
    )
    from app.db import get_table
    table = get_table("products")
    assert table.table_name == "products"
