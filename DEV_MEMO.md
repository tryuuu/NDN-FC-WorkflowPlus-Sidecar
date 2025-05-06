# 開発メモ

NDN-FCW+ の開発・デバッグを行う際のローカル用コマンド・Tips集です。Minikube 上でサイドカーと関数コンテナを使って実験を行う想定です。

## 🔄 Pod の再デプロイ

```bash
kubectl delete -f k8s/pod.yaml
kubectl apply -f k8s/pod.yaml
````

## 🐳 Docker イメージのビルド（Minikube 内）

Minikube の Docker デーモンを使用するため、以下を実行：

```bash
eval $(minikube docker-env)
```

その後、イメージをビルド：

毎回バージョンのタグを変更しないと上書きできないので中止すること。バージョンのタグを変更したら `pod.yaml` も変更する必要がある。

```bash
docker build --no-cache -t ndn-fcw-sidecar:vXX ./sidecar
docker build --no-cache -t function-image:vXX ./function
```

## 🚀 Pod の起動

```bash
kubectl apply -f k8s/pod.yaml
```

## 🛑 Pod の停止

```bash
kubectl delete -f k8s/pod.yaml
```

## 🧾 ログ確認

```bash
kubectl logs -f pod/ndn-func-poc -c ndn-fcw-sidecar
kubectl logs -f pod/ndn-func-poc -c user-function
```

## 🧠 コンテナに入る

```bash
kubectl exec -it ndn-func-poc -c ndn-fcw-sidecar -- bash
kubectl exec -it ndn-func-poc -c user-function -- bash
```

## ✅ 動作確認

```bash
kubectl exec -it ndn-func-poc -c ndn-fcw-sidecar -- bash
python3 consumer.py "/func_demo/data"
python3 consumer.py "/func_demo/(/func_demo/data)"
```

## 🗂️ NLSR 設定ファイルの渡し方

ConfigMap を使って渡す：

```bash
kubectl create configmap nlsr-config --from-file=nlsr.conf=./k8s/nlsr.conf
```

その後、`pod.yaml` 内で以下のように volume として mount：

```yaml
      volumes:
        - name: nlsr-config-volume
          configMap:
            name: nlsr-config
```

```yaml
      volumeMounts:
        - name: nlsr-config-volume
          mountPath: /app/nlsr.conf
          subPath: nlsr.conf
```

## 🧪 その他

* `ndncatchunks` を使ってコンテンツ取得も可能 `例: ndncatchunks "/func_demo/(/func_demo/data)"`
* gRPC proto作成: `python -m grpc_tools.protoc -Iproto --python_out=sidecar --grpc_python_out=sidecar proto/function.proto`
