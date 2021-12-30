#!/bin/bash

echo "=== container stopping ==="
docker stop starcoin-faucet-cron
docker rm  starcoin-faucet-cron
echo "=== container stopped ==="