FROM hydrokhoos/ndn-all:latest

WORKDIR /app

COPY . .

RUN pip install grpcio grpcio-tools protobuf ndn-python-repo


# 実行権限付与
RUN chmod +x entrypoint.sh

ENV NLSR_CONFIG_FILE_PATH=/app/nlsr.conf

ENTRYPOINT ["./entrypoint.sh"]
