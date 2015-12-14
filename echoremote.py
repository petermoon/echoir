#!/home/pi/.virtualenvs/python34/bin/python

import boto3
import boto3.session
import json
from subprocess import call
from time import sleep
import os.path
from botocore.exceptions import ClientError
from botocore.exceptions import BotoCoreError
import logging
LOG_FILENAME = '/home/pi/log/echoremote.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO)


def log(msg):
    logging.info(msg)

sequences = {'all_off': ['tv_off.txt', 'receiver_off.txt',
                         'xbox_off.txt', 'apple_tv_home.txt'],
             'apple_tv': ['tv_on.txt',
                          'receiver_apple_tv.txt',
                          'apple_tv_home.txt'],
             'xbox': ['tv_on.txt', 'receiver_xbox.txt', 'xbox_on.txt'],
             'raspberry_pie': ['tv_on.txt', 'receiver_raspberry_pie.txt'],
             'bluetooth': ['receiver_bluetooth.txt']}
keys = ('ActionA', 'ActionB', 'ActionC', 'ActionD', 'ActionE', 'ActionF')
signals_path = '/home/pi/scribbles/python/echoir/signals/'


def handle_seq(sequence):
    for signal in sequence:
        send_signal(signal)
        sleep(0.2)


def send_signal(signal):
    signal_full = os.path.join(signals_path, signal)
    log('SENT: {}'.format(signal_full))
    if os.path.isfile(signal_full):
        call(['/usr/bin/igclient', '--send', signal_full])
        log("    Sent: {}".format(signal))
    else:
        log("        NOT SENT: {}".format(signal))


def process_msg(msg):
    log(msg.body)
    intent = json.loads(msg.body)
    action = intent['name']
    if action == 'Power':
        handle_power(intent['slots'])
    elif action == 'Volume':
        handle_volume(intent['slots'])
    elif action == 'Launch':
        handle_launch(intent['slots'])
    elif action == 'Action':
        handle_action(intent['slots'])
    msg.delete()


def handle_power(slots):
    device = slots['Device']['value'].replace('the ', '').replace(' ', '_')
    onoff = slots['OnOff']['value']
    if device == 'everything':
        handle_seq(sequences['all_off'])
    else:
        signal = '{}_{}.txt'.format(device, onoff)
        send_signal(signal)


def handle_volume(slots):
    signal = 'receiver_volume_{}.txt'.format(slots['UpDown']['value'])
    try:
        reps = int(slots['Repeat']['value'])
        sequence = [signal for i in range(reps)]
    except (ValueError):
        sequence = [signal]
    handle_seq(sequence)


def handle_launch(slots):
    action = slots['Activity']['value'].replace(' ', '_')
    if action in sequences:
        handle_seq(sequences[action])


def handle_action(slots):
    device = slots['Device']['value'].replace('the ', '').replace(' ', '_')
    device = device.lower()
    sequence = []
    for key in keys:
        if 'value' in slots[key] and slots[key]['value'] is not None:
            sequence.append(slots[key]['value'].replace(' ', '_').lower())
    signals = ['{}_{}.txt'.format(device, a) for a in sequence]
    handle_seq(signals)


url = 'https://queue.amazonaws.com/720549148055/echoRemote'
s = boto3.session.Session(region_name='us-east-1')
queue = s.resource('sqs').Queue(url)


while True:
    try:
        log("Polling for messages...")
        messages = queue.receive_messages(WaitTimeSeconds=20)
        for message in messages:
            log("    Processing a message.")
            process_msg(message)
    except (ClientError, BotoCoreError) as e:
        log("Request failed. Sleeping for a minute.")
        log(str(e))
        sleep(60)
