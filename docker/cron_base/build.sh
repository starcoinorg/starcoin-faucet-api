#!/bin/bash

set -e

IMAGE_NAME="starcoin/starcoin-faucet-cron-base"
IMAGE_LATEST_TAG=$IMAGE_NAME:latest

echo "=== Building  image ${IMAGE_LATEST_TAG} ==="
docker build --no-cache --build-arg GIT_COMMIT=$(git rev-parse HEAD) --build-arg GIT_DIRTY=$(test -n "`git status --porcelain --untracked-files=no`" && echo "+CHANGES" || true) -t $IMAGE_LATEST_TAG -f ../../cron_base.dockerfile ../../
echo "=== Building done ==="