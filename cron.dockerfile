FROM python:3.8

RUN apt-get update && apt-get -y install cron vim

ADD . /app
RUN pip install -r /app/requirements.txt

WORKDIR /app/starcoin-sdk-python
RUN python setup.py install

WORKDIR /app

ENV PYTHONPATH /app

COPY docker/cron/cron.sh /usr/bin/cron.sh
RUN chmod +x /usr/bin/cron.sh

COPY docker/cron/crontab /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab

RUN touch /app/cron.log

ENTRYPOINT ["/bin/sh", "/usr/bin/cron.sh"]