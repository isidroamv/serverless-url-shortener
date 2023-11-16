import json


def generateShortUrl(event, context):
    body = {
        "message": "generateShortUrl",
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response


def getOriginalUrl(event, context):
    body = {
        "message": "getOriginalUrl",
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response

def redirect(event, context):

    response = {"statusCode": 200, "body": "Redirecting..."}

    return response