import asyncio
import os
from typing import Callable, Optional, List
from ndn.app import NDNApp
from ndn.encoding import Name, InterestParam, BinaryStr, FormalName
import logging
import grpc
import function_pb2
import function_pb2_grpc

from lib.ndn_utils import (
    extract_first_level_args,
    extract_my_function_name,
    is_function_request,
    get_data,
)

logging.basicConfig(format='[{asctime}]{levelname}:{message}',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    style='{')


class NDNFunction:
    def __init__(self):
        self.app = NDNApp()
        self.grpc_channel = grpc.insecure_channel('localhost:50051')
        self.grpc_stub = function_pb2_grpc.FunctionRuntimeStub(self.grpc_channel)

    def grpc_function_handler(self, name: str, args: List[bytes]) -> bytes:
        args_str = [arg.decode() for arg in args if arg is not None]
        request = function_pb2.FunctionRequest(name=name, args=args_str)
        response = self.grpc_stub.ExecuteFunction(request)
        return response.result.encode()

    def run(self, prefix: str, data_request_handler: Callable[[str], str]):
        os.system(f"nlsrc advertise {prefix}")

        @self.app.route(prefix)
        def on_interest(name: FormalName, param: InterestParam, _app_param: Optional[BinaryStr]):
            print(f'>> I: {Name.to_str(name)}, {param}', flush=True)

            async def async_on_interest():
                name_str = Name.to_str(name)

                if not is_function_request(name):
                    content = data_request_handler(name_str).encode()
                    self.app.put_data(name, content=content, freshness_period=10000)
                    return

                args = extract_first_level_args(name)
                tasks = [get_data(self.app, arg) for arg in args]
                contents = await asyncio.gather(*tasks)

                # contents に None があると decode で死ぬので対処
                if any(content is None for content in contents):
                    logging.error(f"One or more arguments failed to fetch: {args} -> {contents}")
                    return

                my_function_name = extract_my_function_name(name)
                result = self.grpc_function_handler(my_function_name, contents)

                self.app.put_data(name, content=result, freshness_period=10000)

            asyncio.create_task(async_on_interest())

        self.app.run_forever()
