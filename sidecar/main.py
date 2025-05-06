from concurrent import futures
import grpc
import function_pb2
import function_pb2_grpc

class FunctionRuntimeServicer(function_pb2_grpc.FunctionRuntimeServicer):
    def ExecuteFunction(self, request, context):
        print(f"Sidecar received: name={request.name}, args={request.args}")
        response = f"Hello {request.name}! Args: {', '.join(request.args)}"
        return function_pb2.FunctionResponse(result=response)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    function_pb2_grpc.add_FunctionRuntimeServicer_to_server(FunctionRuntimeServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Sidecar gRPC server started.")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
