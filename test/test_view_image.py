import json
import unittest
from unittest.mock import patch

from src.rest_api.view_image import lambda_handler


def _get_mock_image():
    with open("sample.jpg", "rb") as image:
        return image


class ViewImageTest(unittest.TestCase):

    @patch('src.s3.s3_helper.boto3')
    @patch('src.dynamo.db_helper.boto3')
    def test_lambda_handler_200(self, boto3_dynamo, s3_boto):
        mock_response = {'Items': [{"title": "TestImage",
                                    "description": "A test image",
                                    "userName": "bharat.bajaj",
                                    "fileName": "testfile.jpg"}],
                         'Count': 1, 'ScannedCount': 1,
                         }
        boto3_dynamo.resource.return_value.Table.return_value.query.return_value = mock_response
        s3_boto.client.return_value.get_object.return_value = {'Body': _get_mock_image()}
        event = {'queryStringParameters': {"imageId": "TestImage"}}
        response = lambda_handler(event, None)
        self.assertIsNotNone(response)