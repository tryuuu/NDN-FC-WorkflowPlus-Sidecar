# 🧩 NDN-FCW+ Sidecar Runtime

**NDN-FCW+** は、Named Data Networking (NDN) 上で関数を非同期かつ再帰的に呼び出す分散処理を実現するための基盤です。
本リポジトリはその実行環境として、**NDN通信・ルーティング・トレーシングなどの制御処理を担うサイドカー**と、**ユーザー関数を実装するコンテナ**を分離した構成を提供します。
これにより、関数提供者はネットワーク制御や NDN の詳細に煩わされることなく、**シンプルな Python インターフェースで関数ロジックの記述に集中できる**ようになります。


## 🌐 特徴

- 🧱 **関数をモジュールとして記述するだけ**
- 🧵 **gRPC 経由で NDNSidecar と通信**
- 🔄 **再帰的な Interest 呼び出しに対応**
- 🧩 **セグメント対応（大きなデータも処理可能）**
- 📊 **リクエストチェーンログを MySQL に保存可能**
- 🧪 **Kubernetes 対応・Pod 単位でデプロイ可能**


## 📁 ディレクトリ構成

```

NDN-FCWPlusSidecar/
├── example/           # サンプル実行用（関数 + k8s 構成例）
├── function/          # gRPC ベース関数サーバー用ベース実装
├── proto/             # gRPC の proto 定義
├── sidecar/           # NDN + gRPC サイドカーの実装
├── README.md          # 本ファイル
└── DEV_MEMO.md        # 開発メモ（設計やTODO等）

````


## 🚀 はじめかた（サンプル実行）

```bash
cd example
````

サンプルの手順は以下を参照してください：

📄 [`example/SAMPLE.md`](./example/SAMPLE.md)


## 🛠️ コンポーネント一覧

| コンポーネント     | 説明                                                      |
| ----------- | ------------------------------------------------------- |
| `sidecar/`  | NFD + NLSR 起動・Interest 処理・関数呼び出し・結果返却を行う gRPC サイドカー     |
| `function/` | ユーザーが継承して関数を記述できる gRPC サーバベースイメージ                       |
| `proto/`    | gRPC インターフェース定義（`FunctionRequest` / `FunctionResponse`） |
| `example/`  | サンプルアプリケーションと Kubernetes 用構成                            |


## 🧪 開発・ビルド方法

### 関数ベースイメージ（Function Container）

```bash
cd function
docker build -t harutokobayashi/ndn-fcw-function-base:latest .
docker push harutokobayashi/ndn-fcw-function-base:latest
```

### サイドカーイメージ

```bash
cd sidecar
docker build -t harutokobayashi/ndn-fcw-sidecar:latest .
docker push harutokobayashi/ndn-fcw-sidecar:latest
```


## 📄 使用技術

* [Named Data Networking (NDN)](https://named-data.net/)
* [gRPC](https://grpc.io/)
* [Python 3.10+](https://www.python.org/)
* [Kubernetes](https://kubernetes.io/)
