#!/bin/bash

echo "=== container stopping ==="
docker stop starcoin-faucet-api-cron
docker rm  starcoin-faucet-api-cron
echo "=== container stopped ==="