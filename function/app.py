import grpc
from concurrent import futures
import time

import function_pb2
import function_pb2_grpc


class FunctionRuntimeServicer(function_pb2_grpc.FunctionRuntimeServicer):
    def ExecuteFunction(self, request, context):
        name = request.name
        args = request.args
        print(f"[Function] Received function call: {name}, args: {args}", flush=True)
        result = f"Hello {name}, args: {', '.join(args)}"
        return function_pb2.FunctionResponse(result=result)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    function_pb2_grpc.add_FunctionRuntimeServicer_to_server(FunctionRuntimeServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("Function gRPC Server starting on port 50051...", flush=True)
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    print("Starting Function gRPC Server...", flush=True)
    serve()
