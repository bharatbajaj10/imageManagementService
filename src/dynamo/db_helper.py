import os
import boto3
from boto3.dynamodb.conditions import Key, Attr

table_name = os.getenv('TABLE_NAME', 'image_details')


def save_meta_data_into_db(image_id, image_meta):
    client = boto3.resource('dynamodb')
    table = client.Table(table_name)

    db_record = {
        'imageId': image_id, #partition key
    }
    db_record.update(image_meta)
    table.put_item(Item=db_record)
    return None


def search_image(title, description, user_name, fileName):
    client = boto3.resource('dynamodb')
    table = client.Table(table_name)
    filter_exp = None
    if title:
        filter_exp = Attr("title").eq(title)
    if description:
        condition = Attr("description").eq(description)
        filter_exp = filter_exp & condition if filter_exp is not None else condition
    if user_name:
        condition = Attr("userName").eq(user_name)
        filter_exp = filter_exp & condition if filter_exp is not None else condition
    if fileName:
        condition = Attr("fileName").eq(fileName)
        filter_exp = filter_exp & condition if filter_exp is not None else condition
    result = table.scan(FilterExpression=filter_exp)
    return result['Items']


def query_image(image_id):
    client = boto3.resource('dynamodb')
    table = client.Table(table_name)
    response = table.query(
        KeyConditionExpression=Key('imageId').eq(str(image_id)),
        ProjectionExpression='fileName'
    )
    if response['Count'] > 0:
        return response['Items'][0]
    return None
