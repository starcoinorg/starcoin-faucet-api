FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
# dependencies
COPY . /app

ENV PYTHONPATH /app

RUN pip install -r /app/requirements.txt

ENTRYPOINT uvicorn app.main:app --reload --host 0.0.0.0