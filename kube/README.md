# faucet-api

## start/restart pods

kubectl apply -f ./faucet-api-deployment.yaml

## check pods

kubectl get pods
NAME READY STATUS RESTARTS AGE
faucet-api-deployment-6bd5b7d999-mmk47 1/1 Running 0 52s

## check logs

kubectl logs -f faucet-api-deployment-6bd5b7d999-mmk47

or

kubectl get pods|grep 'faucet-api-deployment' |grep -v grep |awk -F' ' '{print $1}' | xargs kubectl logs -f

## start service

kubectl apply -f ./service-faucet-api.yaml

## check service

kubectl get services
NAME TYPE CLUSTER-IP EXTERNAL-IP PORT(S) AGE
faucet-api LoadBalancer xxxx xxx.elb.amazonaws.com 80:30570/TCP 4m48s

## cname https://api-faucet.starcoin.org to xxx.elb.amazonaws.com

# faucet-cron

## start/restart pods

kubectl apply -f ./faucet-cron-deployment.yaml

## check pods

kubectl get pods
NAME READY STATUS RESTARTS AGE
faucet-cron-deployment-54cc7476bd-l76rr 1/1 Running 0 7m16s

## check logs

kubectl logs -f faucet-cron-deployment-54cc7476bd-l76rr

or

kubectl get pods|grep 'faucet-cron-deployment' |grep -v grep |awk -F' ' '{print $1}' | xargs kubectl logs -f
