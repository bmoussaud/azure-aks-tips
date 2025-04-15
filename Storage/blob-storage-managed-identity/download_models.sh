#!/bin/bash
set -x 
IP=$(kubectl get svc nginx --namespace app-routing-system -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
TARGET='shared'
MODEL='microsoft_bitnet-b1.58-2B-4T'
echo "IP: ${IP}"
curl http://${IP}/download/model/${MODEL}/target/${TARGET}