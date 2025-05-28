import sys
import os
from ndn_function_grpc import NDNFunction

def data_request_handler(name: str) -> str:
    print(f"Interest: {name}")
    return "DATA"

if __name__ == '__main__':
    # if len(sys.argv) < 3:
    #     print("Usage: python main.py <prefix> <namespace>")
    #     sys.exit(1)
        
    print("Starting NDN gRPC Server...")
    # prefix = sys.argv[1]
    # namespace = sys.argv[2]
    user_name = os.getenv('USER_NAME', 'default')
    prefix = f"/{user_name}/func_demo"
    namespace = "default"
    ndn = NDNFunction()
    # ndn.run(prefix,namespace, data_request_handler)
    ndn.run(prefix, data_request_handler)
