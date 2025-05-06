FROM python:3.10-slim

WORKDIR /app

COPY function_pb2.py /app/
COPY function_pb2_grpc.py /app/
COPY server.py /app/

RUN pip install grpcio grpcio-tools

ENTRYPOINT ["python3", "/app/server.py"]
