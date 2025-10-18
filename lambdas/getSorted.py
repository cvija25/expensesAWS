import json
import boto3
from decimal import Decimal

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('expenses')

    params = event.get('queryStringParameters', {}) or {}
    sort_key = params.get('key', 'price')

    response = table.scan()
    items = response.get('Items', [])

    items.sort(key=lambda x: x.get(sort_key, 0))

    def decimal_default(obj):
        if isinstance(obj, Decimal):
            return float(obj)
        raise TypeError

    return {
        'statusCode': 200,
        'body': json.dumps(items, default=decimal_default)
    }