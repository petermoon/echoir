import json
import logging
from random import randint
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

with open('config.json') as config_file:
    config = json.load(config_file)

sqs = boto3.resource('sqs', region_name='us-east-1')
queue = sqs.Queue(config['queue_url'])


def lambda_handler(event, context):
    app_id = event['session']['application']['applicationId']
    logger.info('Application ID: {}'.format(app_id))
    if app_id not in config['skills']:
        raise Exception('Invalid application ID')

    if event['request']['type'] == 'LaunchRequest':
        handle_launch(config['skills'][app_id])
    if event['request']['type'] == 'IntentRequest':
        if config['skills'][app_id] == 'remote':
            handle_remote(event['request'])
        else:
            handle_action(config['skills'][app_id], event['request'])
    resp = build_ssml_response(get_random_speech())
    logger.info('Response: {}'.format(resp))
    return resp


def handle_launch(activity):
    msg = {
        'name': 'Launch',
        'slots': {
            'Activity': {
                'name': 'Activity',
                'value': activity
            }
        }
    }
    send_message(json.dumps(msg))


def handle_remote(req):
    """
    Handles power and volume intents from the generic remote skill
    """
    send_message(json.dumps(req['intent']))


def handle_action(device, req):
    """
    Passes through intent requests from device-specific skills
    after setting the device name
    """
    intent = req['intent']
    intent['slots']['Device'] = {'name': 'Device', 'value': device}
    send_message(json.dumps(intent))


def send_message(body):
    queue.send_message(MessageBody=body)


def build_ssml_response(speech):
    resp = {
        'version': '1.0',
        'response': {
            'outputSpeech': {
                'type': 'SSML',
                'ssml': speech
            },
            'shouldEndSession': True
        }
    }
    return resp


def get_random_speech():
    num_responses = len(config['responses'])
    return config['responses'][randint(0, num_responses - 1)]
