#!/bin/bash
#set -x 
IP=$(kubectl get svc nginx --namespace app-routing-system -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
TARGET='container'
echo "IP: ${IP}"
echo 
curl -s -X POST http://${IP}:80/write-content/${TARGET}/file/1M/size/1 |jq 
curl -s -X POST http://${IP}:80/write-content/${TARGET}/file/10M/size/10 | jq
curl -s -X POST http://${IP}:80/write-content/${TARGET}/file/100M/size/100 | jq
curl -s -X POST http://${IP}:80/write-content/${TARGET}/file/1G/size/1000 | jq
curl -s -X POST http://${IP}:80/write-content/${TARGET}/file/10G/size/10000   
