import json
import boto3
import os

dynamodb = boto3.client('dynamodb')
table_name = 'batch12_uday_stock_level'

def process_item(item):
    processed_item = {}
    processed_item['product_id'] = item['Item']['product_id']['S']
    processed_item['quantity'] = int(item['Item']['quantity']['N'])
    processed_item['location'] = item['Item']['location']['S']
    return processed_item
    

def lambda_handler(event, context):
    print("Loading Uday RetrieveStockLevels Function")\

    try:
        product_id = event['pathParameters']['product_id']
        print(f"Been asked to retrieve stock levels for {product_id}")
    except (KeyError, TypeError) as e:
        product_id = None
        print("Oops! No product ID specified. Will get'em all!")
        
    if product_id is not None:
        item = dynamodb.get_item(
            TableName=table_name,
            Key={
                "product_id": {
                    "S": product_id
                }
            })
        print(f"From DB, got item = {item}")
    
        if "Item" not in item:
            return {
                'statusCode': 404,
                'body': ''
            }
        else:
            processed_item = process_item(item)
        return {
            'statusCode': 200,
            'body': json.dumps(processed_item)
        }
    else:
        try:
            # Scan the table and get all items
            table = boto3.resource('dynamodb').Table(table_name)
            response = table.scan()
            items = response['Items']
            return {
            'statusCode': 200,
            'body': {
                    "Status": "Data Retrieved Successfully",
                    "Response":items
                }
            }
        except Exception as e:
            print(e)
            return {
                "statusCode": 500,
                "body": json.dumps('Error Retrieving data')
            }
        
            
