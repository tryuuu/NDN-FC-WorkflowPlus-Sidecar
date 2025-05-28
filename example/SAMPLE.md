
# ✨ NDN-FCW+ サンプル実行手順

この `example` ディレクトリには、NDN-FCW+ サイドカーと連携して動作する「関数コンテナのサンプル」が含まれています。

## 📦 ディレクトリ構成

```

example/
├── app/
│   ├── Dockerfile      ← ユーザー関数用 Dockerfile（ベースを継承）
│   └── handler.py      ← 実装する関数（main を定義するだけ！）
├── k8s/
│   ├── nlsr.conf       ← サンプル用 NLSR 設定ファイル
│   └── pod.yaml        ← NDN サイドカー + ユーザー関数の Pod 構成

````

---

## 🛠️ サンプル実行までの手順

以下の手順に従えば、あなたの関数をすぐに NDN 経由で呼び出すことができます。

---

### ① `handler.py` に関数を実装する

```python
# app/handler.py

def main(name: str, args: list[str]) -> str:
    return f"Hello {name}! Args: {', '.join(args)}"
````

---

### ② Docker イメージをビルド & Push

```bash
cd example/app

# Docker Hub 上に push したいイメージ名を指定
docker build -t tryuu/ndn-fcw-function-demo:latest .
docker push tryuu/ndn-fcw-function-demo:latest
```

```bash
cd sidecar
docker build -t tryuu/ndn-fcw-sidecar:latest .
docker push tryuu/ndn-fcw-sidecar:latest
```

※ `harutokobayashi` の部分はご自身の Docker Hub アカウントに置き換えてください。

---

### ③ NLSR 設定ファイルを ConfigMap に登録

```bash
cd ../k8s

kubectl delete configmap nlsr-config --ignore-not-found
kubectl create configmap nlsr-config --from-file=nlsr.conf
```

---

### ④ `pod.yaml` を編集

* 自分が push した関数イメージ名に変更します
* サイドカーに渡す prefix も自由に変更できます（例: `/func_demo`）

```yaml
containers:
  - name: ndn-fcw-sidecar
    image: harutokobayashi/ndn-fcw-sidecar:latest
    env:
      - name: NDN_FUNCTION_PREFIX
        value: "/func_demo"  # <- ここで指定した名前が Interest 名のプレフィックスになります
  - name: user-function
    image: harutokobayashi/ndn-fcw-function-demo:latest  # <- 自分の関数イメージにする
```

---

### ⑤ Pod を起動

```bash
# あらかじめ起動しているpodを削除しておく
kubectl delete -f pod.yaml
kubectl apply -f pod.yaml
```

---

### ⑥ 動作確認（Interest の送信）

この Pod 単体で NDN-FCW+ の動作確認が可能です。

```bash
kubectl exec -it ndn-func-demo -c ndn-fcw-sidecar -- \
  python3 consumer.py "/func_demo/(/func_demo/data)"
```

* このリクエストに対して、関数コンテナ内の `main(name, args)` が実行され、結果が NDN 経由で返ってきます。
* `/func_demo/data` はファンクションに同封されているサンプルレスポンスです。サンプル用に `Producer` としての役割も持っています。

---

## 🧼 クリーンアップ

```bash
kubectl delete pod ndn-func-demo
kubectl delete configmap nlsr-config
```

---

## 🚀 仕組みの概要

NDN-FCW+ サイドカー（`ndn-fcw-sidecar`）が以下を担当します：

* NFD + NLSR の起動・設定
* Interest のパース
* 必要な引数の再帰フェッチ
* gRPC 経由で関数を呼び出し、結果を返却（セグメント対応）

ユーザーは **`handler.py` に main 関数を書くだけ** で、NDN 関数を定義できます。