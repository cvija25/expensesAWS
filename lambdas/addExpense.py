import json
import boto3
import uuid
from decimal import Decimal

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('expenses')

    body = json.loads(event.get('body', '{}'))

    required_fields = ['name', 'category', 'amount', 'price', 'time']
    if not all(f in body for f in required_fields):
        return {
            'statusCode': 400,
            'body': json.dumps({'message': f'Missing one of: {required_fields}'})
        }

    item = {
        'id': str(uuid.uuid4()),
        'name': body['name'],
        'category': body['category'],
        'amount': Decimal(str(body['amount'])),
        'price': Decimal(str(body['price'])),
        'time': body['time']
    }

    table.put_item(Item=item)

    return {
        'statusCode': 201,
        'body': json.dumps({'message': 'Expense added', 'item': item}, default=str)
    }