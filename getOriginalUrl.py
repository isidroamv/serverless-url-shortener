import json
import boto3
import os

ddb = boto3.resource('dynamodb').Table(os.environ['DYNAMODB_TABLE'])

"""
Retrieves the original URL associated with a given short URL.

Args:
    event (dict): The event data passed to the function.
    context (dict): The runtime information of the function.

Returns:
    dict: A dictionary containing the HTTP status code and, if successful, the original URL.

        - If the short URL is missing or invalid, returns {"statusCode": 400}.
        - If the short URL is valid but not found in the database, returns {"statusCode": 404}.
        - If the short URL is valid and found in the database, returns {"statusCode": 200, "body": {"originalUrl": str}}.
"""
def getOriginalUrl(event, context):
    queryParameters = event.get('queryStringParameters')
    
    if not queryParameters or not queryParameters['shortUrl']:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "Missing short URL"
            })
        }

    shortUrl = queryParameters['shortUrl']
    if not shortUrl.startswith(os.environ['API_URL']):
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "Invalid short URL"
            })
        }

    shortId = shortUrl.replace(os.environ['API_URL'] + '/', '')
    ddb_response = ddb.get_item(Key={'shortId': shortId})

    if ddb_response.get('Item') is None:
        response = {"statusCode": 404}
    else:
        response = {
            "statusCode": 200, 
            "body": json.dumps({
                "originalUrl": ddb_response.get('Item')['originalUrl']
            })
        }

    return response