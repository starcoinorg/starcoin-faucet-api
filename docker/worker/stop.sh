#!/bin/bash

echo "=== container stopping ==="
docker stop starcoin-faucet-api-worker
docker rm  starcoin-faucet-api-worker
echo "=== container stopped ==="