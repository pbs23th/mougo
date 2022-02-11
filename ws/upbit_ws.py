import websocket
import requests
import json
# import sqlsetting
import pymysql
from datetime import datetime
import redis

# 중요한 값은 상수사용합니다.
SYMBOL_LIST_ENDPOINT = "https://api.upbit.com/v1/market/all"
# ENDPOINT = "wss://ws.bitmex.com/realtime"
ENDPOINT = "wss://api.upbit.com/websocket/v1"
rd = redis.StrictRedis(host='localhost', port=6379, db=0)

def sendRequest(url):
    markets = requests.get(url).json()
    market_data = []
    for market in markets:
        if market['market'][:3] == "KRW":
            market_data.append(market['market'])
    return market_data

def getBitmexSymbolList(contents):
    # symbol_list = [
    #       pair['symbol']
    #       for pair in contents
    #      ]
    # symbol_list = ["KRW-BTC"]
    # contents안에 들어있는 각각의 아이템들 중에서
    # 키가 symbol인 것들만 리스트에 넣겠다는 뜻

    # formatted_list = [ '{}'.format(symbol) for symbol in symbol_list]
    #  {"op":"subscribe", "args" : []}의 형식이었죠? args에 formatted_list를
    #  웹서버로 보내주면 bitmex에서 제공하는 모든 symbol에 대한 OHLCV를 얻을 수 있습니다.

    # return {"op":"subscribe", "args" : formatted_list}
    return [{"ticket":"test"},{"type":"ticker","codes":contents}]

list_data = dict()
def on_message(ws, message):
    my_dict = json.loads(message)
    # ws.close(status=websocket.STATUS_PROTOCOL_ERROR)
    if 'code' in my_dict:
        code = my_dict['code']
        # jsonDataDict = json.dumps(my_dict, ensure_ascii=False).encode('utf-8')
        trade_price = my_dict['trade_price']
        # rd.set(code,jsonDataDict)
    #     symbol = my_dict['data'][0]['symbol']
    #     timestamp = my_dict['data'][0]['timestamp']
        rd.set('upbit:'+code, trade_price)
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
    contents = sendRequest(SYMBOL_LIST_ENDPOINT)
    symbols = getBitmexSymbolList(contents)
    print(symbols)
    ws.send(json.dumps(symbols))


def run(endpoint):
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(endpoint,
                                on_open = on_open,
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close,
                                on_ping=on_ping,
                                on_pong=on_pong)

    ws.run_forever(ping_interval=60, ping_timeout=10,ping_payload='PING')

if __name__ == "__main__":
    run(ENDPOINT)
    # sendRequest(SYMBOL_LIST_ENDPOINT)
