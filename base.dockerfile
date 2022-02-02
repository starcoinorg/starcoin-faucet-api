FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

RUN apt-get update && apt-get -y install cron vim

COPY . /app
RUN pip install -r /app/requirements.txt

WORKDIR /app/starcoin-sdk-python
RUN python setup.py install

WORKDIR /app