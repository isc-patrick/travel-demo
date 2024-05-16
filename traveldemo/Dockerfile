FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get -y install gcc mono-mcs && \
    rm -rf /var/lib/apt/lists/* 

RUN apt-get update && \
    apt-get -y install software-properties-common

RUN  add-apt-repository ppa:deadsnakes/ppa && \
     apt-get update

#RUN apt-get -y install unixodbc-dev

RUN apt-get -y install git

RUN apt-get -y install python3.11
RUN apt-get -y install python3-pip && \
    pip install --upgrade pip && \
    pip install --upgrade setuptools

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY bin /tmp/bin
RUN pip install /tmp/bin/intersystems_irispython-3.2.0-py3-none-any.whl

# COPY data /data 
# COPY scripts /scripts
# COPY config /config

RUN mkdir /traveldemo
WORKDIR /traveldemo
COPY . .
RUN pip install -e .

# Easiest way to get model into local cache
RUN python3 -c "from sentence_transformers import SentenceTransformer; model = SentenceTransformer('all-MiniLM-L6-v2');"

WORKDIR /traveldemo/traveldemo

#CMD ["python3","-m","panel","serve","app.py","--allow-websocket-origin=0.0.0.0:8123","--address","0.0.0.0","--port","8123","--autoreload", "--admin"]

ENTRYPOINT [ "../start_panel.sh"]
