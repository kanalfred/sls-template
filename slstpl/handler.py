import json
import time
from slstpl.s3 import S3Storage, StorageItemNotFound
from slstpl.util.logger import logger
import boto3
import os
import uuid

s3 = S3Storage()


def about(event, context):
    # return {"message": "Go Curiosity!", "version": os.environ.get('SLS_COMPONENT_VERSION', 'local')}

    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!####",
        # "input": event
        "input": "very cool!"
    }
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }
    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """

def demo(event, context):
    # get path parameter
    #    event['pathParameters']['id']
    # post/put data
    #    event["body"]

    body = {
        "message": "akan test response yeah",
        # "input": event
        "input": "very cool!## fast"
    }
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }
    return response


def save_s3(event, context):
    key = 'demo/test2.json'

    # save s3
    s3.json[key] = {"apple": "test3a", "boy": "test3b"}
    # load s3
    saved_json = s3.json[key]

    response = {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "s3 saved!",
                "saved_json" : saved_json
            }
        )
    }
    return response


def save_nosql(event, context):
    timestamp = str(time.time())
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    # data = json.loads(event['body'])
    uid = str(uuid.uuid1())

    item = {
        'id': uid,
        'text': 'save data test3!',
        'checked': False,
        'createdAt': timestamp,
        'updatedAt': timestamp,
    }

    # write to dynamodb
    table.put_item(Item=item)

    # get from dynamodb
    result = table.get_item(
        Key={
            'id': uid
        }
    )

    response = {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "dynamodb saved!",
                "saved": result['Item']
            }
        )
    }
    return response


# for debug
if __name__ == "__main__":
        demo('', '')
