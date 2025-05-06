
### コンテナに入る

```
kubectl exec -it ndn-func-poc -c ndn-fcw-sidecar -- bash
kubectl exec -it ndn-func-poc -c user-function -- bash
```

### kubectl 起動/停止

```
kubectl apply -f k8s/pod.yaml
kubectl delete -f k8s/pod.yaml
```

### ログを見る

```
kubectl logs -f pod/ndn-func-poc -c ndn-fcw-sidecar
kubectl logs -f pod/ndn-func-poc -c user-function
```

## 動作確認

```
kubectl exec -it ndn-func-poc -c ndn-fcw-sidecar -- bash
python3 consumer.py "/func_nodeX/data"
python3 consumer.py "/func_nodeX/(/func_nodeX/data)"
```

### nlsr.conf

```
kubectl create configmap nlsr-config --from-file=nlsr.conf=./k8s/nlsr.conf
```