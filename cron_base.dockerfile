FROM python:3.8

RUN apt-get update && apt-get -y install cron vim

ADD . /app
RUN pip install -r /app/requirements.txt
