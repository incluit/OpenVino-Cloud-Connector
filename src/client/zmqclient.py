# client.py
import zmq
import sys
import time
import logging
import os

HOST = '127.0.0.1'
PORT = '4444'

logging.basicConfig(filename='../../logs/subscriber.log', level=logging.INFO)


class ZClient(object):

    def __init__(self, host=HOST, port=PORT):
        """Initialize Worker"""
        self.host = host
        self.port = port
        self._context = zmq.Context()
        self._subscriber = self._context.socket(zmq.SUB)
        print("Client Initiated")

    def receive_message(self):
        """Start receiving messages"""
        self._subscriber.connect('tcp://{}:{}'.format(self.host, self.port))
        self._subscriber.setsockopt(zmq.SUBSCRIBE, b"")

        while True:
            print('listening on tcp://{}:{}'.format(self.host, self.port))
            message = self._subscriber.recv()
            print(message)
            logging.info(
                '{}   - {}'.format(message, time.strftime("%Y-%m-%d %H:%M")))


    def follow(thefile):
        thefile.seek(0,2) # Go to the end of the file
        while True:
            line = thefile.readline()
            if not line:
                time.sleep(0.1) # Sleep briefly
                continue
            yield line
            print (line + ' Se copio!!!')


if __name__ == '__main__':
    zs = ZClient()
    zs.receive_message()
    zs.follow('../../logs/subscriber.log')
