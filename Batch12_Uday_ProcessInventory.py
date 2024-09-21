import json
import boto3
import os
import copy

dynamodb = boto3.client('dynamodb')

def create_new_item(item):
    new_item = copy.deepcopy(item)
    del new_item['timestamp']
    del new_item['update_type']
    return new_item
    
def update_existing_item(current_item, item):
    print("Loading Uday Process Function")
    print(f"Current Item = {current_item}")
    print(f"Incoming Item = {item}")
    new_item = copy.deepcopy(item)
    if item['update_type']['S'] == "ADD_STOCK":
        new_item['quantity']['N'] = str(int(current_item['quantity']['N']) + int(item['quantity']['N']))
        
    if item['update_type']['S'] == "REMOVE_STOCK":
        new_item['quantity']['N'] = str(int(current_item['quantity']['N']) - int(item['quantity']['N']))
    
    print("Adjusting keys.")        
    del new_item['timestamp']
    del new_item['update_type']
    print(f"New Item = {new_item}")
        
    return new_item
    

def lambda_handler(event, context):
    table_name = 'batch12_uday_stock_level'
    responses = []
    
    print("Hello!  Triggered by SQS queue and received below records.")
    print(event['Records'])
    for record in event['Records']:
        print(record['body'])
        #item = json.loads(record['body'])['ValidatedNewEntry']
        item = json.loads(record['body'])['body']['message']['ValidatedNewEntry']
        print(item)
        product_id = item['product_id']['S']
        print(product_id)
        current_item = dynamodb.get_item(
            TableName=table_name,
            Key={
                'product_id': {
                    'S': product_id
                }
            }
        )
        print("Checked IF product already exists.")
        print(f"Got = {current_item}")
        
        if "Item" not in current_item:
            print("This is a new item. Creating entry.")
            new_item = create_new_item(item)
        else:
            print("Item already exists. So, updating")
            new_item = update_existing_item(current_item['Item'], item)
        
        response = dynamodb.put_item(
            TableName=table_name,
            Item=new_item
        )
        responses.append(response)
        print(f"Item ingested = {item}")
        print(f"Response received = {response}")
        
    return {
        'statusCode': 200,
        'body': json.dumps(responses)
    }
