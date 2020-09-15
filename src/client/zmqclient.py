# client.py
from datetime import datetime

import zmq
import sys
import time
import logging
import os

HOST = '127.0.0.1'
PORT = '4444'

logging.basicConfig(filename='logs/subscriber.log', level=logging.INFO)

class ZClient(object):

    def __init__(self, host=HOST, port=PORT):
        """Initialize Worker"""
        self.host = host
        self.port = port
        self._context = zmq.Context()
        self._subscriber = self._context.socket(zmq.SUB)
        print("Client Initiated")

    def receive_message(self,count = 1):
        """Start receiving messages"""
        self._subscriber.connect('tcp://{}:{}'.format(self.host, self.port))
        self._subscriber.setsockopt(zmq.SUBSCRIBE, b"")

        while True:
            print('listening on tcp://{}:{}'.format(self.host, self.port))
            message = self._subscriber.recv().decode("utf-8")
            print(message)
            logging.info(
                '{}   - {}'.format(message, time.strftime("%Y-%m-%d %H:%M")))
            count +=1
            Esearch().hit_kibana(message, count)


from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import boto3

regionaws = 'us-east-1'  # e.g. us-west-1
hostaws = 'search-driver-management-2lzumo4geewhdzwcxsqnoacrmy.us-east-1.es.amazonaws.com'  # For example, my-test-domain.us-east-1.es.amazonaws.com


class Esearch(object):

    @staticmethod
    def hit_kibana(message, count):
        service = 'es'
        credentials = boto3.Session().get_credentials()
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
            "precision": l[5]
        }

        count +=1

        es.index(index="alerts", doc_type="_doc", id=count, body=document)

        print(es.get(index="alerts", doc_type="_doc", id=count))


if __name__ == '__main__':
    zs = ZClient()
    zs.receive_message()
