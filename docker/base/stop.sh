#!/bin/bash

echo "=== container stopping ==="
docker stop starcoin-faucet-base
docker rm  starcoin-faucet-base
echo "=== container stopped ==="