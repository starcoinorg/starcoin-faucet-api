FROM python:3.8

ADD . /app
RUN pip install -r /app/requirements.txt

WORKDIR /app/starcoin-sdk-python
RUN python setup.py install

WORKDIR /app

ENV C_FORCE_ROOT True
ENV PYTHONPATH /app

ENTRYPOINT celery worker -A app.worker -E --loglevel=info