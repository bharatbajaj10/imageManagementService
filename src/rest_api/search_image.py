import json
import logging
import os
import traceback

from src.dynamo import db_helper


logger = logging.getLogger()
logger.setLevel(os.getenv('LOGGING_LEVEL', 'WARN'))


def lambda_handler(event, context=None):
    logger.debug("Event Received: %s", str(event))
    try:
        request_body_json = event.get('body', None)
        if request_body_json is None:
            raise ValueError({
                "Invalid request - Missing required input(s)",
            })
        request_body_json = json.loads(request_body_json)
        return _process_request(request_body_json)

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


def _process_request(request_body_json):
    title = request_body_json.get("title")
    description = request_body_json.get("description")
    user_name = request_body_json.get("userName")
    fileName = request_body_json.get("fileName")

    results = db_helper.search_image(title, description, user_name, fileName)

    return {
        "statusCode": 200,
        "body": json.dumps(results)
    }
