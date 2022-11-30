import json
import unittest
from unittest.mock import patch

from src.rest_api.search_image import lambda_handler


class SearchImageTest(unittest.TestCase):

    @patch('src.dynamo.db_helper.boto3')
    def test_lambda_handler_200(self, boto3_dynamo):
        mock_response = {'Items': [{"title": "TestImage",
                                    "description": "A test image",
                                    "userName": "bharat.bajaj",
                                    "fileName": "testfile.jpg"}],
                         'Count': 1, 'ScannedCount': 1,
                         }
        boto3_dynamo.resource.return_value.Table.return_value.scan.return_value = mock_response
        body = json.dumps({"title": "TestImage",
                           "description": "A test image",
                           "userName": "bharat.bajaj"})
        event = {'body': body}
        response = lambda_handler(event, None)
        self.assertIsNotNone(response)
        self.assertEqual(200, response['statusCode'])
        self.assertIsNotNone(response['body'])