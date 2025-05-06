import grpc
from concurrent import futures
import function_pb2
import function_pb2_grpc
import importlib.util
import sys
import os

HANDLER_PATH = "/app/handler.py"

# handler.py の存在チェック
if not os.path.exists(HANDLER_PATH):
    print(f"❌ ERROR: {HANDLER_PATH} が見つかりませんでした。", file=sys.stderr)
    print("このベースイメージを使うには handler.py を /app に配置してください。", file=sys.stderr)
    print("\n📘 例: handler.py", file=sys.stderr)
    print("""
def main(name: str, args: list[str]) -> str:
    return f"Hello {name}! Args: {', '.join(args)}"
""", file=sys.stderr)
    sys.exit(1)

# handler.py をロード
spec = importlib.util.spec_from_file_location("handler", HANDLER_PATH)
handler = importlib.util.module_from_spec(spec)
spec.loader.exec_module(handler)

# main 関数の存在チェック
if not hasattr(handler, "main"):
    print("❌ ERROR: handler.py に main(name: str, args: list[str]) -> str が定義されていません。", file=sys.stderr)
    print("関数インターフェースは以下の形式で定義してください：", file=sys.stderr)
    print("""
def main(name: str, args: list[str]) -> str:
    return "result string"
""", file=sys.stderr)
    sys.exit(1)


class FunctionRuntimeServicer(function_pb2_grpc.FunctionRuntimeServicer):
    def ExecuteFunction(self, request, context):
        print(f"[Function] Executing: {request.name}, args={request.args}", flush=True)
        try:
            result = handler.main(request.name, list(request.args))
            return function_pb2.FunctionResponse(result=result)
        except Exception as e:
            print(f"❌ ERROR in user function: {e}", file=sys.stderr)
            return function_pb2.FunctionResponse(result=f"Error: {str(e)}")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    function_pb2_grpc.add_FunctionRuntimeServicer_to_server(FunctionRuntimeServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("✅ Function gRPC Server started on port 50051", flush=True)
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
