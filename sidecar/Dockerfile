FROM hydrokhoos/ndn-all:latest

WORKDIR /app

COPY . .

RUN pip install grpcio grpcio-tools protobuf ndn-python-repo


# 実行権限付与
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
