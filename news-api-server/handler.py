import json


def hello(event, context):
    body = {
        "message": "Hello, babo babo",
        "event" : event,
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response
