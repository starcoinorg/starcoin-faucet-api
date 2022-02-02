## docker starcoin-faucet-base

1. stop container，delete old container

`./stop.sh`

2. build docker image

`./build.sh`

4. check log

`docker logs -f starcoin-faucet-base`

5. One-click for all above

`./rebuild.sh`

6. tag
   `docker tag starcoin/starcoin-faucet-base:latest starcoin/starcoin-faucet-base:0.3.0`

7. publish to docker hub
   `docker push starcoin/starcoin-faucet-base:0.3.0`
