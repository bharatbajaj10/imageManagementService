import json
import logging
import os
import traceback

from src.dynamo import db_helper
from src.s3 import s3_helper


logger = logging.getLogger()
logger.setLevel(os.getenv('LOGGING_LEVEL', 'WARN'))


def lambda_handler(event, context=None):
    logger.debug("Event Received: %s", str(event))
    try:
        query_string_params = event.get('queryStringParameters', None)
        if query_string_params is None:
            raise ValueError({
                "Invalid request - Missing required input(s)",
            })
        image_id = query_string_params.get('imageId')
        if not image_id:
            raise ValueError({
                "Invalid request - Image Id is required parameter.",
            })
        return _process_request(image_id)

    except ValueError as ve:
        logger.error(ve)
        return {
            "statusCode": 400,
            "body": ve
        }

    except Exception as ex:
        traceback.print_exc()
        logger.error(ex)
        response = {
            "message": "EXCEPTION processing Request",
            "exceptionTrace": str(ex)
        }
        return {
            "statusCode": 500,
            "body": json.dumps(response)
        }


def _process_request(image_id):
    file_name = db_helper.query_image(image_id)
    if not file_name:
        return {
            "statusCode": 404,
            "body": "Image not found"
        }

    image_str = s3_helper.download_image(file_name)
    return {
        "statusCode": 200,
        "body": image_str
    }
