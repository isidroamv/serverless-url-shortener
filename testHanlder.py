# test_lambda_function.py
import unittest
import handler

class TestLambdaFunction(unittest.TestCase):
    def test_generate_short_url(self):
        # Arrange
        event = {"originalUrl": "http://example.com"}
        context = {}

        # Act
        result = handler.generateShortUrl(event, context)

        # Assert
        self.assertEqual(result, {'statusCode': 200, 'body': '{"message": "generateShortUrl"}'})

    def test_get_original_url(self):
        # Arrange
        event = {"shortUrl": "https://xxxxxxxxx.execute-api.us-east-1.amazonaws.com/dubqe"}
        context = {}

        # Act
        result = handler.getOriginalUrl(event, context)

        # Assert
        self.assertEqual(result, {'statusCode': 200, 'body': '{"message": "getOriginalUrl"}'})

    def test_redirect(self):
        # Arrange
        event = {"pathParams:": {"shortId": "dubqe"}}
        context = {}

        # Act
        result = handler.redirect(event, context)

        # Assert
        self.assertEqual(result, {'statusCode': 200, 'body': 'Redirecting...'})

if __name__ == '__main__':
    unittest.main()
