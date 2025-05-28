import logging
import sys
import os
from ndn.app import NDNApp
from ndn.types import InterestNack, InterestTimeout, InterestCanceled, ValidationFailure
from ndn.encoding import Name
from lib.ndn_utils import get_data

logging.basicConfig(format='[{asctime}]{levelname}:{message}',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    style='{')

app = NDNApp()

async def main():
    if len(sys.argv) < 2:
        print("Usage: python consumer.py <interest-name>")
        app.shutdown()
        return

    user_name = os.getenv('USER_NAME', 'default')
    interest_name = user_name + "/" + sys.argv[1]

    try:
        # インタレストパケットを送信
        content = await get_data(app, interest_name)
        print(bytes(content) if content else None)
    except InterestNack as e:
        print(f'Nacked with reason={e.reason}')
    except InterestTimeout:
        print('Timeout')
    except InterestCanceled:
        print('Canceled')
    except ValidationFailure:
        print('Data failed to validate')
    finally:
        app.shutdown()

if __name__ == '__main__':
    app.run_forever(after_start=main())
