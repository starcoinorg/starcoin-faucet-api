#!/bin/bash
CURDIR=$(cd "$(dirname "$0")"; pwd)
docker run -d --name starcoin-faucet-api-cron \
    -e "STARCOIN_FAUCET_DEBUG=${STARCOIN_FAUCET_DEBUG}" \
    -e "STARCOIN_FAUCET_CELERY_REDIS_BROKER_ADDRESS=${STARCOIN_FAUCET_CELERY_REDIS_BROKER_ADDRESS}" \
    -e "STARCOIN_FAUCET_CELERY_REDIS_BACKEND_ADDRESS=${STARCOIN_FAUCET_CELERY_REDIS_BACKEND_ADDRESS}" \
    -e "STARCOIN_FAUCET_REDIS_DSN=${STARCOIN_FAUCET_REDIS_DSN}" \
    -e "STARCOIN_FAUCET_MYSQL_HOST=${STARCOIN_FAUCET_MYSQL_HOST}" \
    -e "STARCOIN_FAUCET_MYSQL_PORT=${STARCOIN_FAUCET_MYSQL_PORT}" \
    -e "STARCOIN_FAUCET_MYSQL_USER=${STARCOIN_FAUCET_MYSQL_USER}" \
    -e "STARCOIN_FAUCET_MYSQL_PWD=${STARCOIN_FAUCET_MYSQL_PWD}" \
    -e "STARCOIN_FAUCET_MYSQL_DB=${STARCOIN_FAUCET_MYSQL_DB}" \
    -e "STARCOIN_FAUCET_PRIVATE_KEY_BARNARD=${STARCOIN_FAUCET_PRIVATE_KEY_BARNARD}" \
    -e "STARCOIN_FAUCET_PRIVATE_KEY_PROXIMA=${STARCOIN_FAUCET_PRIVATE_KEY_PROXIMA}" \
    -e "STARCOIN_FAUCET_PRIVATE_KEY_HALLEY=${STARCOIN_FAUCET_PRIVATE_KEY_HALLEY}" \
    starcoin/starcoin-faucet-api-cron:latest

docker ps


