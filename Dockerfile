FROM python:3.8-slim

RUN apt-get update && apt-get -y upgrade && apt-get autoremove

RUN apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        zip unzip \
        sudo

RUN pip3 install pyzmq
RUN pip3 install Flask
RUN pip3 install boto3
RUN pip3 install elasticsearch
RUN pip3 install requests
RUN pip3 install requests-aws4auth
RUN pip3 --no-cache-dir install --upgrade awscli

ADD . /app
WORKDIR /app

COPY aws/ /root/.aws

RUN ["chmod", "+x", "scripts/process.sh"]

CMD ["scripts/process.sh"]
