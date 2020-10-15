FROM python:3.8-slim

RUN apt-get update && apt-get -y upgrade && apt-get autoremove

RUN apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        zip unzip \
        sudo \
        wget \
        gcc \
        git \
        vim

#CMAKE to install EIS message bus 

RUN wget https://cmake.org/files/v3.15/cmake-3.15.0-Linux-x86_64.sh
RUN mkdir /opt/cmake
RUN bash cmake-3.15.0-Linux-x86_64.sh --prefix=/opt/cmake --skip-license
RUN update-alternatives --install /usr/bin/cmake cmake /opt/cmake/bin/cmake 1 --force


RUN pip3 install pyzmq
RUN pip3 install cython
RUN pip3 install Flask
RUN pip3 install boto3
RUN pip3 install elasticsearch
RUN pip3 install requests
RUN pip3 install requests-aws4auth
RUN pip3 --no-cache-dir install --upgrade awscli

# EIS message bus
ADD . /app
WORKDIR /app/src/common/
RUN bash /app/src/common/eis_libs_installer.sh
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib/
# --------------


WORKDIR /app

RUN ["chmod", "+x", "scripts/process.sh"]

CMD ["scripts/process.sh"]
