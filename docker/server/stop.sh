#!/bin/bash

echo "=== container stopping ==="
docker stop starcoin-faucet-api-server
docker rm  starcoin-faucet-api-server
echo "=== container stopped ==="