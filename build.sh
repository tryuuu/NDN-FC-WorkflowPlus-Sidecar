#!/bin/bash

# プロトコル定義生成
python -m grpc_tools.protoc -Iproto --python_out=sidecar --grpc_python_out=sidecar proto/function.proto
cp sidecar/function_pb2*.py function/

# ビルド
docker build --no-cache -t sidecar-image ./sidecar
docker build --no-cache -t function-image ./function


# Minikube に転送
minikube image load sidecar-image --overwrite
minikube image load function-image --overwrite

# Apply pod
kubectl delete -f k8s/pod.yaml
kubectl apply -f k8s/pod.yaml

# ログ確認
# kubectl logs pod/ndn-func-poc -c sidecar
# kubectl logs pod/ndn-func-poc -c function
