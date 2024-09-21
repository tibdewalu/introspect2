import json
import uuid
from pprint import pprint

def validate_quantity(updated_item):
    return (int(updated_item['quantity']['N']) > 0)
    
def validate_update_type(updated_item):
    if updated_item['update_type']['S'] == "ADD_STOCK":
        return True
    elif updated_item['update_type']['S'] == "REMOVE_STOCK":
        return True
    else:
        return False

def lambda_handler(event, context):
    print("Loading Batch12_Uday_Validate_Inventory function and below event is RECEIVED")
    print(event)
    
    updated_item = event.get('NewImage', None)
    if updated_item is not None:
        quantity_valid = validate_quantity(updated_item)
        print(f"Quantity Valid = {quantity_valid}")
        update_type_valid = validate_update_type(updated_item)
        print(f"Update Type Valid = {update_type_valid}")
    
    if updated_item is None or quantity_valid is False or update_type_valid is False:
        response = {
            "flag": "Invalid",
            "message": "You should not see such a message in SQS."
        }
    else:
        response = {
            "flag": "Valid",
            "message": {
                "ValidatedNewEntry": updated_item
            },
            "MessageId": str(uuid.uuid4())
        }

    return {
        'statusCode': 200,
        'body': response
    }
