## docker starcoin-faucet-cron-base

1. stop container，delete old container

`./stop.sh`

2. build docker image

`./build.sh`

4. check log

`docker logs -f starcoin-faucet-cron-base`

5. One-click for all above

`./rebuild.sh`

6. inspect a running container.
   `docker exec -it <CONTAINER_ID> /bin/bash`

7. tag
   `docker tag starcoin/starcoin-faucet-cron-base:latest starcoin/starcoin-faucet-cron:0.2.0`

8. publish to docker hub
   `docker push starcoin/starcoin-faucet-cron-base:0.2.0`