import os

import boto3


def get_dynamodb_resource():
    return boto3.resource("dynamodb", region_name=os.environ.get("AWS_DEFAULT_REGION", "ap-southeast-1"))


def get_table(table_name: str):
    return get_dynamodb_resource().Table(table_name)