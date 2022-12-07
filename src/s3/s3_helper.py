import os

import boto3
import base64


BUCKET = os.getenv('BUCKET_NAME', 'matt-s3-test')


def upload_image_to_s3(image_id, file_name, decoded_image):
    s3_client = boto3.client('s3')
    s3_client.put_object(Body=decoded_image, Bucket=BUCKET, Key=file_name)


def download_image(file_name):
    s3_client = boto3.client('s3')
    data = s3_client.get_object(Bucket=BUCKET, Key=file_name)
    contents = data['Body'].read()
    return _encode_image_into_base64(contents)


def _encode_image_into_base64(image_content):
    return base64.b64encode(image_content)