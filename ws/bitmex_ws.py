import websocket
import json
from datetime import datetime
import redis

rd = redis.StrictRedis(host='localhost', port=6379, db=0)
# 중요한 값은 상수사용합니다.
SYMBOL_LIST_ENDPOINT = "https://www.bitmex.com/api/v1/instrument/active"
# ENDPOINT = "wss://ws.testnet.bitmex.com/realtime"
ENDPOINT = "wss://ws.bitmex.com/realtime"


def getBitmexSymbolList():
    symbol_list = ["XBTUSD", "XBTH22"]
    formatted_list = [ 'trade:{}'.format(symbol) for symbol in symbol_list]
    return {"op":"subscribe", "args" : formatted_list}

list_data = dict()
def on_message(ws, message):
    my_dict = json.loads(message)
    if 'data' in my_dict:
        ticker = my_dict['data'][0]['price']
        symbol = my_dict['data'][0]['symbol']
        rd.set('bitmex:'+symbol, ticker)
    else:
        pass

def on_ping(ws, message):
    print("Got a ping! A pong reply has already been automatically sent.")
    print(message)

def on_pong(ws, message):
    print("Got a pong! No need to respond")
    print(message)


def on_error(ws, error):
    print(error)
    ws.on_close(ws)

def on_close(ws):
    print("### closed ###")
    print(datetime.now())
    ws.close()

def on_open(ws):
    print("### open ###")
    symbols = getBitmexSymbolList()
    ws.send(json.dumps(symbols))

def run(endpoint):
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(endpoint,
                                on_open = on_open,
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close,
                                on_ping=on_ping,
                                on_pong=on_pong
                                )

    ws.run_forever(ping_interval=60, ping_timeout=10,ping_payload='PING')

if __name__ == "__main__":
    run(ENDPOINT)