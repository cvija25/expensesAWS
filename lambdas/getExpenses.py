import json
import boto3
from decimal import Decimal

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('expenses')
    response = table.scan()
    items = response.get('Items', [])

    def decimal_default(obj):
        if isinstance(obj, Decimal):
            return float(obj)
        raise TypeError

    return {
        'statusCode': 200,
        'body': json.dumps(items, default=decimal_default)
    }