FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
# dependencies
COPY . /app

WORKDIR /app/starcoin-sdk-python
RUN python setup.py install

WORKDIR /app

ENV PYTHONPATH /app

RUN pip install -r /app/requirements.txt

ENTRYPOINT uvicorn app.main:app --reload --host 0.0.0.0