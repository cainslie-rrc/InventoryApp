import json
import boto3
import uuid
import os
from decimal import Decimal

def lambda_handler(event, context):
    # Parse incoming JSON data

    try:
        body = event.get('body')
        if body is None:
            raise ValueError("Missing body")

        # If body is already a dict, don't parse again
        if isinstance(body, dict):
            data = body
        else:
            data = json.loads(body)

    except Exception:
        return {
            'statusCode': 400,
            'body': json.dumps("Bad request. Please provide the data.")
        }

    # try:
    #     data = json.loads(event['body'])
    # except KeyError:
    #     return {
    #         'statusCode': 400,
    #         'body': json.dumps("Bad request. Please provide the data.")
    #     }

    # Get the table name from environment variable
    table_name = os.getenv('TABLE_NAME', 'Inventory')

    # DynamoDB setup
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    # Generate a unique ID
    unique_id = str(uuid.uuid4())

    # Insert data into DynamoDB
    try:
        table.put_item(
            Item={
                'id': unique_id,
                'location_id': data['location_id'],
                'description': data['description'],
                'name': data['name'],
                'price': Decimal(str(data['price'])),
                'qty': data['qty'],
            }
        )
        return {
            'statusCode': 200,
            'body': json.dumps(f"Item with ID {unique_id} added successfully.")
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error adding item: {str(e)}")
        }