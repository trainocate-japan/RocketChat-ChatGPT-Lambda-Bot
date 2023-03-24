import json
import os
import logging
import trainocate_util
import boto3
import requests
from botocore.exceptions import ClientError
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all
patch_all()

logger = logging.getLogger()
logger.setLevel(trainocate_util.logger_level())
parameter_content = os.environ.get('PARAMETER_CONTENT')
parameter_apikey = os.environ.get('PARAMETER_KEY')
openai_endpoint = os.environ.get('OPENAI_ENDPOINT')

def get_parameter(parameter_name):
    ssm = boto3.client('ssm')
    try:
        response = ssm.get_parameter(
            Name=parameter_name,
            WithDecryption=True
        )
        return response['Parameter']['Value']
    except ClientError as e:
        if e.response['Error']['Code'] == 'ParameterNotFound':
            print("Parameter not found: %s" % e)
        else:
            raise

def get_reply(text, system_content, apikey):

    payload = {
        'model': 'gpt-3.5-turbo',
        'messages': [
            {'role': 'system', 'content': system_content},
            {'role': 'user', 'content': text}
        ]
    }

    headers = {
        'Content-type': 'application/json',
        'Authorization': 'Bearer ' + apikey
    }

    try:
        response = requests.post(
            openai_endpoint,
            data=json.dumps(payload),
            headers=headers
        )
        data = response.json()
        logger.debug(data)
        return_text = data['choices'][0]['message']['content']
        return return_text
    except:
        raise

def lambda_handler(event, context):
    logger.debug(event)
    try:
        body = json.loads(event['body'])
        text = body['text']
        logger.debug(text)
        system_content = get_parameter(parameter_content)
        apikey = get_parameter(parameter_apikey)

        reply = get_reply(text, system_content, apikey)
        logger.debug(reply)
        payload = {"text": reply}
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps(payload)
        }

    except Exception as e:
        raise e
