#!/bin/bash

VERSION=v8

kubectl delete -f k8s/pod.yaml

# ビルド
docker build --no-cache -t ndn-fcw-sidecar:v15 ./ndn-fcw-sidecar
docker build --no-cache -t function-image:v15 ./function

# Apply pod
kubectl apply -f k8s/pod.yaml

# ログ確認
# kubectl logs pod/ndn-func-poc -c ndn-fcw-sidecar
# kubectl logs pod/ndn-func-poc -c user-function
