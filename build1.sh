#!/bin/bash

VERSION=v7

kubectl delete -f k8s/pod.yaml

# Minikube の中で docker を動かす
eval $(minikube docker-env)

# ビルド
docker build --no-cache -t ndn-fcw-sidecar:v12 ./ndn-fcw-sidecar

# Minikube に転送
# minikube image load ndn-fcw-sidecar:v7

# Apply pod
kubectl apply -f k8s/pod.yaml

# ログ確認
# kubectl logs pod/ndn-func-poc -c ndn-fcw-sidecar
# kubectl logs pod/ndn-func-poc -c user-function       
# ndncatchunks 