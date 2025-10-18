import json
import boto3
from boto3.dynamodb.conditions import Attr
from decimal import Decimal
from datetime import datetime

def normalize_date(date_str):
    parts = date_str.split('-')
    year = parts[0]
    month = parts[1].zfill(2)
    day = parts[2].zfill(2)
    return f"{year}-{month}-{day}"

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('expenses')

    params = event.get('queryStringParameters') or {}
    date_from = params.get('from')
    date_to = params.get('to')

    if not date_from or not date_to:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Missing from/to parameters'})
        }

    try:
        response = table.scan()
        items = response.get('Items', [])

        filtered_items = []
        for item in items:
            normalized_time = normalize_date(item['time'])
            if date_from <= normalized_time <= date_to:
                filtered_items.append(item)

        def decimal_default(obj):
            if isinstance(obj, Decimal):
                return float(obj)
            raise TypeError

        return {
            'statusCode': 200,
            'body': json.dumps(filtered_items, default=decimal_default)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error', 'error': str(e)})
        }