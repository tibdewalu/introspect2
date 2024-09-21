import json
import boto3
import os

sf = boto3.client('stepfunctions')

def lambda_handler(event, context):

    execution_ids = []
    for record in event['Records']:
        print('Loading Batch12_Uday_Stream_DynamoDB Function')
        print(record['eventID'])
        print(record['eventName'])
        print("DynamoDB Record: " + json.dumps(record['dynamodb'], indent=2))
        
        response = sf.start_execution(
            stateMachineArn='arn:aws:states:ap-south-1:569445711959:stateMachine:Batch12_Uday_StateMachine',
            input=json.dumps(record['dynamodb'])
        )
        execution_ids.append(response['executionArn'])
        
    return f"Scheduled following state functions runs = {execution_ids}"
