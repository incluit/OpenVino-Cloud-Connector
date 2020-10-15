# client.py
from datetime import datetime

import sys
import time
import logging
import os
import time
import json
import argparse
import eis.msgbus as mb

from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import boto3

logging.basicConfig(filename='logs/subscriber.log', level=logging.INFO)
regionaws = 'us-east-1'  # e.g. us-west-1
hostaws = 'search-driver-management-2lzumo4geewhdzwcxsqnoacrmy.us-east-1.es.amazonaws.com'  # For example, my-test-domain.us-east-1.es.amazonaws.com
msgbus = None
subscriber = None
count = 1
credentials = boto3.Session().get_credentials()

class Esearch(object):

    @staticmethod
    def hit_kibana(message, count):
        service = 'es'
        if credentials is None or credentials.access_key is None:
            print("You need to configure the credentials.")
            return
        awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, regionaws, service,
                           session_token=credentials.token)
        l = message.split(",");

        es = Elasticsearch(
            index='alerts',
            hosts=[{'host': hostaws, 'port': 443}],
            http_auth=awsauth,
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection
        )

        date_time_str = l[1] + ' ' + l[2]
        date_time_obj = datetime.strptime(date_time_str, '%d/%m/%Y %H:%M:%S')

        document = {
            "service": l[0],
            "date": date_time_obj,
            "time": l[2],
            "camera": l[3],
            "event": l[4],
            "precision": l[5],
            "dr_mode": l[6]
        }

        count +=1

        es.index(index="alerts", doc_type="_doc", id=count, body=document)

# Argument parsing
ap = argparse.ArgumentParser()
ap.add_argument('config', help='JSON configuration')
ap.add_argument('-t', '--topic', default='BLAS', help='Topic')
ap.add_argument('-p', '--print', default=False, action='store_true',
                help='Print the received message')
args = ap.parse_args()

with open(args.config, 'r') as f:
    config = json.load(f)

try:
    print('[INFO] Initializing message bus context')
    msgbus = mb.MsgbusContext(config)

    print(f'[INFO] Initializing subscriber for topic \'{args.topic}\'')
    subscriber = msgbus.new_subscriber(args.topic)

    print('[INFO] Running...')
    while True:
        msg = subscriber.recv()
        meta_data, blob = msg
        if meta_data is not None:
            if args.print:
                payload = msg.get_name()+","+meta_data["message"]
                print(f'[INFO] RECEIVED: message: {payload}')
                logging.info('{}   - {}'.format(payload, time.strftime("%Y-%m-%d %H:%M")))
                count +=1
                if len(payload.split(",")) == 7:
                    Esearch().hit_kibana(payload, count)

except KeyboardInterrupt:
    print('[INFO] Quitting...')
finally:
    if subscriber is not None:
        subscriber.close()
