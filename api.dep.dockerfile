FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
# dependencies
COPY starcoin-sdk-python /app/starcoin-sdk-python
COPY requirements.txt /app/requirements.txt

RUN cd starcoin-sdk-python && python setup.py install

ENV PYTHONPATH /app

RUN pip install -r /app/requirements.txt
