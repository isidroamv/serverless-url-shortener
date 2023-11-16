# test_lambda_function.py
import unittest
from unittest import TestCase
from unittest.mock import patch
from moto import mock_dynamodb
from generateShortUrl import generateShotId
import json
import boto3


ENV_VARS = {
    'DYNAMODB_TABLE': 'dynamodbTable',
    'API_URL': 'https://xxxxxxxxx.execute-api.us-east-1.amazonaws.com'
}
@patch.dict('os.environ', ENV_VARS, clear=True)
class TestLambdaFunction(TestCase):

    @mock_dynamodb
    @patch('generateShortUrl.generateShotId')
    def test_shorten_url_flow(self, mock_generateShotId):
        import generateShortUrl
        import getOriginalUrl
        dynamodb = boto3.resource('dynamodb')
        dynamodb.create_table(TableName="dynamodbTable", 
            KeySchema=[{'AttributeName': 'shortId','KeyType': 'HASH'}], 
            AttributeDefinitions=[{'AttributeName': 'shortId','AttributeType': 'S'}],
            BillingMode='PAY_PER_REQUEST')
        
        # Data to mock the generateShotId function
        mock_generateShotId.side_effect = [
            'abcde', # Id for Step 1
            'abcde', # Id for Step 2
            'vwxyz'  # Id for Step 2 when becase the id already exists
        ]

        
        # Step 1: Generate the short URL
        event = {"body": json.dumps({"originalUrl": "http://example.com"})}
        context = {}
        result = generateShortUrl.generateShortUrl(event, context)
        self.assertEqual(result, {'statusCode': 200, 'body': '{"shortUrl": "https://xxxxxxxxx.execute-api.us-east-1.amazonaws.com/abcde"}'})

        # Step 2: Generate the short URL with a different original URL
        event = {"body": json.dumps({"originalUrl": "http://example2.com"})}
        context = {}
        result = generateShortUrl.generateShortUrl(event, context)        
        self.assertEqual(result, {'statusCode': 200, 'body': '{"shortUrl": "https://xxxxxxxxx.execute-api.us-east-1.amazonaws.com/vwxyz"}'})
        self.assertEqual(mock_generateShotId.call_count, 3)



    @patch('boto3.resource')
    def test_get_original_url(self, mock_boto3_resource):
        import getOriginalUrl

        mock_dynamodb = mock_boto3_resource().Table()
        mock_dynamodb.get_item.side_effect = [
            {'Item': None},
            {'Item': {
                'shortId': 'abcde',
                'originalUrl': 'https://example.com'
            }}
        ]

        # Assert the status code is 404 when the short URL is not found
        event = {"queryStringParameters": {"shortUrl": "https://xxxxxxxxx.execute-api.us-east-1.amazonaws.com/vwxyz"}}
        context = {}
        result = getOriginalUrl.getOriginalUrl(event, context)
        self.assertEqual(result.get('statusCode'), 404)
        
        # Assert the status code is 200 when the short URL is found
        event = {"queryStringParameters": {"shortUrl": "https://xxxxxxxxx.execute-api.us-east-1.amazonaws.com/abcde"}}
        context = {}
        result = getOriginalUrl.getOriginalUrl(event, context)
        self.assertEqual(result.get('statusCode'), 200)


    # Test the redirect function
    @patch('boto3.resource')
    def test_redirect(self, mock_boto3_resource):
        import handleRedirect
        # Arrange
        mock_boto3_resource().Table().get_item.side_effect = [
            {'Item': None},
            {'Item': {
                'shortId': 'abcde',
                'originalUrl': 'https://example.com'
            }}
        ]

        # Act - Call the redirect function when the short URL is not found
        event = {"pathParameters": {"shortId": "vwxyz"}}
        context = {}
        result = handleRedirect.redirect(event, context)
        self.assertEqual(result.get('statusCode'), 404)

        # Act - Call the redirect function when the short URL is found
        event = {"pathParameters": {"shortId": "dubqe"}}
        context = {}
        result = handleRedirect.redirect(event, context)
        self.assertEqual(result, {
            'body': 'Redirecting to https://example.com',
            'headers': {'Location': 'https://example.com'},
            'statusCode': 302
            }
        )

if __name__ == '__main__':
    unittest.main()
