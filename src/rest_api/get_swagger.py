
import json
import os

import yaml


def lambda_handler(event, context=None):
    swagger = get_swagger_file()
    with open(swagger, 'r') as stream:
        data_loaded = yaml.load(stream)
        response = {
            "body": json.dumps(data_loaded),
            "statusCode": 200
        }
        return response


def get_swagger_file():
    swagger_file_name = 'swagger.yaml'
    for filename in os.listdir("."):
        filename_ = filename.lower()
        if (('swagger' in filename_)):
            swagger_file_name = filename
            break
    return swagger_file_name