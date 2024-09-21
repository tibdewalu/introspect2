import json
import boto3
import datetime

client = boto3.client('dynamodb')
dynamodb = boto3.resource('dynamodb')
TABLE_NAME = 'batch12_uday_inventory_update'

def lambda_handler(event, context):
    print('event:', event)
    body = event.get('body')
    if not body:
        return {
            'statusCode': 400,
            'body': json.dumps("Check if request body is MISSING ! ! !")
        }
    print('body: ', body)
    inventory = json.loads(body);
    
    # Store data in DynamoDB
    inventoryUpdateTable = dynamodb.Table(TABLE_NAME)

    product_id = inventory['product_id']
    quantity = inventory['quantity']
    location = inventory['location']
    timestamp = datetime.datetime.now().isoformat()
    update_type = inventory['update_type']
    item = {
        'product_id': product_id,
        'quantity': int(quantity),
        'location': location,
        'timestamp': timestamp,
        'update_type': update_type
    }
    inventoryUpdateTable.put_item(Item=item)
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Inventory Updated Successfully'})
    }
