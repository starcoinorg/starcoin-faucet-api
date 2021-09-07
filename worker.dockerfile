FROM python:3.8

ADD app /data/app
COPY requirements.txt /data/app
RUN pip install -r /data/app/requirements.txt

WORKDIR /data

ENV PYTHONPATH /data

ENTRYPOINT celery worker -A app.worker -E --loglevel=info