import json
import boto3


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


# for debug
if __name__ == "__main__":
        demo('', '')
