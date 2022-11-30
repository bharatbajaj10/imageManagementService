import logging
import os
import json
import traceback
import cuid
import base64
from datetime import datetime, date
from src.dynamo import db_helper
from src.s3 import s3_helper


logger = logging.getLogger()
logger.setLevel(os.getenv('LOGGING_LEVEL', 'WARN'))
BUCKET = os.getenv('BUCKET_NAME', 'myBucket')


def get_current_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")


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
    image_str = request_body_json.get("image")
    user_name = request_body_json.get("userName")
    if any([
        any([title is None, title == '',]),
        any([description is None, description == '']),
        any([image_str is None, image_str == '', ]),
    ]):
        raise ValueError({
            "Invalid request - Missing required input(s)",
        })

    image_id: str = cuid.cuid()
    todays_date = date.today()
    file_name = BUCKET + "/" + str(todays_date.year) + "/" + str(todays_date.month) + "/" + str(
        todays_date.day) + "/" + image_id + ".jpg"

    decoded_image = _decode_image_from_body(image_str)
    image_meta = {
        "title": title,
        "description": description,
        "userName": user_name,
        "uploadedTime": get_current_timestamp(),
        "fileName": file_name
        # other metadata here...
    }

    db_helper.save_meta_data_into_db(image_id, image_meta)
    s3_helper.upload_image_to_s3(image_id, file_name, decoded_image)

    msg = {"message": "Image saved successfully"}
    return {
        "statusCode": 200,
        "body": json.dumps(msg)
    }


def _decode_image_from_body(image_str):
    return base64.b64decode(image_str.encode("utf-8"))

