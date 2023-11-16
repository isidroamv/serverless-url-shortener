import json
import boto3
import os


ddb = boto3.resource('dynamodb').Table(os.environ['DYNAMODB_TABLE'])

"""
Redirects the user to the original URL based on the given short ID.

Parameters:
    event (dict): The event containing the path parameters.
    context (object): The context object.

Returns:
    dict: The response object containing the status code, body, and headers.
        If the short ID is not found, returns a response with a status code of 404.
        If the short ID is found, returns a response with a status code of 302,
        a body indicating the redirect URL, and a "Location" header with the redirect URL.
"""
def redirect(event, context):
    shorId = event.get('pathParameters')["shortId"]
    if not shorId:
        return {
            "statusCode": 404,
        }
    
    ddb_response = ddb.get_item(Key={'shortId': shorId})

    if ddb_response.get('Item') is None:
        response = {"statusCode": 404}
    else:
        response = {
            "statusCode": 302, 
            "body": "Redirecting to " + ddb_response.get('Item')['originalUrl'],
            "headers": {
                "Location": ddb_response.get('Item')['originalUrl']
            }
        }

    return response