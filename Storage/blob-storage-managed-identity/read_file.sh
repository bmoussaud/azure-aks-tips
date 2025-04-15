#!/bin/bash
#set -x 
IP=$(kubectl get svc nginx --namespace app-routing-system -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
TARGET='shared'
echo "IP: ${IP}"

curl -s  http://${IP}:80/write-content/${TARGET}/file/1M |jq 
curl -s  http://${IP}:80/write-content/${TARGET}/file/10M | jq
curl -s  http://${IP}:80/write-content/${TARGET}/file/100M | jq
curl -s  http://${IP}:80/write-content/${TARGET}/file/1G | jq
curl -s  http://${IP}:80/write-content/${TARGET}/file/10G | jq   
