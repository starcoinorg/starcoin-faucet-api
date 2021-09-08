#!/bin/bash

echo "=== container stopping ==="
docker stop starcoin-faucet-api
docker rm  starcoin-faucet-api
echo "=== container stopped ==="