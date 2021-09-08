# faucet-api

## start/restart pods
kubectl apply -f ./faucet-api-deployment.yaml

## check pods
$kubectl get pods                       
NAME                                               READY   STATUS    RESTARTS   AGE
faucet-api-deployment-847564d655-j8xpw            1/1     Running   0          7m16s

## check logs
kubectl logs -f faucet-api-deployment-847564d655-j8xpw

## start service
kubectl apply -f ./service-faucet-api.yaml

## check service 
$kubectl get services 
NAME                   TYPE           CLUSTER-IP       EXTERNAL-IP             PORT(S)        AGE
faucet-api            LoadBalancer   xxxx             xxx.elb.amazonaws.com   80:30570/TCP   4m48s

##  cname https://api-faucet.starcoin.org to xxx.elb.amazonaws.com

# faucet-cron

## start/restart pods
kubectl apply -f ./faucet-cron-deployment.yaml

## check pods
$kubectl get pods                       
NAME                                               READY   STATUS    RESTARTS   AGE
faucet-cron-deployment-847564d655-j8xpw            1/1     Running   0          7m16s

## check logs
kubectl logs -f faucet-cron-deployment-847564d655-j8xpw
