FROM starcoin/starcoin-faucet-base:latest

COPY . /app

ENV PYTHONPATH /app

ENTRYPOINT uvicorn app.main:app --reload --host 0.0.0.0