import json
from slstpl.s3 import S3Storage, StorageItemNotFound
from slstpl.util.logger import logger
# import boto3

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
    s3.json[key] = {"apple": "test1", "boy": "test2"}

    response = {
        "statusCode": 200,
        "body": json.dumps(
            {"message": "s3 saved!"}
        )
    }
    return response


def save_nosql(event, context):
    response = {
        "statusCode": 200,
        "body": json.dumps(
            {"message": "dynamodb saved!"}
        )
    }
    return response


# for debug
if __name__ == "__main__":
        demo('', '')
