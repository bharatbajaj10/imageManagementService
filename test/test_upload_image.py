import json
import unittest
from unittest.mock import patch
import base64

from src.rest_api.upload_image import lambda_handler


def _get_image_str():
    with open("sample.jpg", "rb") as image:
        return base64.b64encode(image.read()).decode("utf-8")


class UploadImageTest(unittest.TestCase):

    @patch('src.dynamo.db_helper.boto3')
    @patch('src.s3.s3_helper.boto3')
    def test_lambda_handler_200(self, boto3_dynamo, boto_s3):
        boto3_dynamo.resource.return_value.Table.return_value.put_item.return_value = None
        boto_s3.client.return_value.put_object.return_value = None
        body = json.dumps({"title": "TestImage",
                           "description": "A test image",
                           "userName": "bharat.bajaj",
                           "image": _get_image_str()})
        event = {'body': body}
        response = lambda_handler(event, None)
        self.assertIsNotNone(response)
        self.assertEqual(200, response['statusCode'])