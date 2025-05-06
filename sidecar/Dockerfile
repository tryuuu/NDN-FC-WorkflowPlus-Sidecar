FROM python:3.10-slim

WORKDIR /app
COPY . .
RUN pip install grpcio grpcio-tools

CMD ["python", "main.py"]
