FROM python:3.8

RUN apt-get update && apt-get -y install cron vim

COPY ./requirements.txt /app
RUN pip install -r /app/requirements.txt

COPY ./starcoin-sdk-python /app
WORKDIR /app/starcoin-sdk-python
RUN python setup.py install

WORKDIR /app