import grpc
import function_pb2
import function_pb2_grpc
import time

time.sleep(1)  # サイドカー待機

channel = grpc.insecure_channel('localhost:50051')
stub = function_pb2_grpc.FunctionRuntimeStub(channel)

request = function_pb2.FunctionRequest(name='greet', args=['Alice', 'Bob'])
response = stub.ExecuteFunction(request)

print(f"Function got response: {response.result}")
