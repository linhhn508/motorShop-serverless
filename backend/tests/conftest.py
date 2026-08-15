import os

import boto3
import pytest
from moto import mock_aws

os.environ.setdefault("AWS_DEFAULT_REGION", "ap-southeast-1")
os.environ.setdefault("AWS_ACCESS_KEY_ID", "testing")
os.environ.setdefault("AWS_SECRET_ACCESS_KEY", "testing")
os.environ.setdefault("JWT_SECRET", "test-secret-key-at-least-32-bytes!!")
os.environ.setdefault("ADMIN_USERNAME", "admin")
os.environ.setdefault("ADMIN_PASSWORD", "admin123")
os.environ.setdefault("PRODUCTS_TABLE", "products")
os.environ.setdefault("FEEDBACK_TABLE", "feedback")
os.environ.setdefault("CONTACTS_TABLE", "contacts")


@pytest.fixture(scope="function")
def aws_mock():
    with mock_aws():
        yield


@pytest.fixture(scope="function")
def dynamodb_tables(aws_mock):
    ddb = boto3.resource("dynamodb", region_name="ap-southeast-1")

    products_table = ddb.create_table(
        TableName="products",
        KeySchema=[{"AttributeName": "productId", "KeyType": "HASH"}],
        AttributeDefinitions=[
            {"AttributeName": "productId", "AttributeType": "S"},
            {"AttributeName": "category", "AttributeType": "S"},
        ],
        GlobalSecondaryIndexes=[
            {
                "IndexName": "category-index",
                "KeySchema": [{"AttributeName": "category", "KeyType": "HASH"}],
                "Projection": {"ProjectionType": "ALL"},
            }
        ],
        BillingMode="PAY_PER_REQUEST",
    )

    feedback_table = ddb.create_table(
        TableName="feedback",
        KeySchema=[
            {"AttributeName": "productId", "KeyType": "HASH"},
            {"AttributeName": "createdAt", "KeyType": "RANGE"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "productId", "AttributeType": "S"},
            {"AttributeName": "createdAt", "AttributeType": "S"},
        ],
        BillingMode="PAY_PER_REQUEST",
    )

    contacts_table = ddb.create_table(
        TableName="contacts",
        KeySchema=[{"AttributeName": "contactId", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "contactId", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST",
    )

    return {"products": products_table, "feedback": feedback_table, "contacts": contacts_table}


@pytest.fixture(scope="function")
def flask_client(dynamodb_tables):
    from app import create_app
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(scope="function")
def admin_token():
    import jwt
    return jwt.encode(
        {"sub": os.environ["ADMIN_USERNAME"], "role": "admin"},
        os.environ["JWT_SECRET"],
        algorithm="HS256",
    )
