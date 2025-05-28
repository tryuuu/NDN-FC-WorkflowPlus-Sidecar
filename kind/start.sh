#! /bin/bash
kind create cluster --config cluster.yaml --name kindcluster
kubectl cluster-info --context kind-kindcluster
kubectl create configmap nlsr-config --from-file=nlsr.conf
# kind delete cluster --name kindcluster