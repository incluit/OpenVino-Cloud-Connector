#!/bin/bash

# turn on bash's job control
set -m

# Start the client process
python3 /app/src/client/msgBusClient.py /app/src/client/configs/tcp_subscriber_no_security.json --print