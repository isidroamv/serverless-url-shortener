import json
import boto3
import string
import random
import os

"""
Generate a random 5-character string consisting of lowercase letters.
Returns:
    str: A randomly generated 5-character string.
"""
def generateShotId():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(5))


"""
Generates a short URL for a given original URL.

Args:
    event (dict): The event object containing the request details.
    context (object): The context object containing the runtime information.

Returns:
    dict: The response object containing the status code and the short URL.

Raises:
    None
"""
def generateShortUrl(event, context):
    ddb = boto3.resource('dynamodb').Table(os.environ['DYNAMODB_TABLE'])

    body = json.loads(event['body'])

    if body is None or body['originalUrl'] is None:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "Missing original URL"
            })
        }
    
    shortId = generateShotId()

    # Check if the id already exists in the database
    while True:
        if ddb.get_item(Key={'shortId': shortId}).get('Item'):
            shortId = generateShotId()
        else:
            break

    ddb.put_item(
        Item={
            'shortId': shortId,
            'originalUrl': body['originalUrl']
        }
    )

    response = {
        "statusCode": 200,
        "body": json.dumps({
            "shortUrl": os.environ['API_URL'] + "/" + shortId
        })
    }

    return response

