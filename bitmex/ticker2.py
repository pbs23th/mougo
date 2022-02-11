import websocket
import requests
import json
import sqlsetting
import pymysql

# 중요한 값은 상수사용합니다.
SYMBOL_LIST_ENDPOINT = "https://www.testnet.com/api/v1/instrument/active"
# ENDPOINT = "wss://ws.testnet.bitmex.com/realtime"
ENDPOINT = "wss://ws.testnet.bitmex.com/realtime"

def sendRequest(url):
    # print('1')
    # res = requests.get(url)
    # print('2')
    # contents = res.content.decode('utf-8')
    # python2에서는 contents = res.content만 적어도 됩니다.
    # python2에서는 res.content가 string으로 오지만
    # python3에서는 byte로 오기 때문에 디코딩이 필요합니다.

    # 대부분의 api는 json으로 반환되기 때문에 곧바로 json 라이브러리를 이용해 로드합니다
    # json_contents = json.loads(contents)
    json_contents = {"pair" : {'symbol' :["XBTUSD", "XBTH22"]}}
    return json_contents

def getBitmexSymbolList(contents):
    # symbol_list = [
    #       pair['symbol']
    #       for pair in contents
    #      ]
    symbol_list = ["XBTUSD", "XBTUSDT", "XBTEUR", "XBTUSDTZ21", "XBTZ21", "XBTH22", "XBTX21", "XBTEURZ21"]
    # contents안에 들어있는 각각의 아이템들 중에서
    # 키가 symbol인 것들만 리스트에 넣겠다는 뜻

    formatted_list = [ 'trade:{}'.format(symbol) for symbol in symbol_list]
    #  {"op":"subscribe", "args" : []}의 형식이었죠? args에 formatted_list를
    #  웹서버로 보내주면 bitmex에서 제공하는 모든 symbol에 대한 OHLCV를 얻을 수 있습니다.

    return {"op":"subscribe", "args" : formatted_list}

def on_message(ws, message):
    my_dict = json.loads(message)
    if 'data' in my_dict:
        ticker = my_dict['data'][0]['price']
        symbol = my_dict['data'][0]['symbol']
        timestamp = my_dict['data'][0]['timestamp']
        if symbol not in list_data:
            list_data[f'{symbol}'] = ticker
        print(f'{symbol} : ' ,ticker)
        if list_data[f'{symbol}'] != ticker:
            ticker_update(timestamp, symbol,ticker)
        else:
            pass


def ticker_update(timestamp, symbol,ticker):
    connection = sqlsetting.mysqlset()
    my_cursor = connection.cursor(pymysql.cursors.DictCursor)
    sql = '''update trade.bitmex_price set timestamp = %s, price = %s where market = %s '''
    my_cursor.execute(sql, (str(timestamp), float(ticker), symbol))
    connection.commit()
    connection.close()



def on_error(ws, error):
    print(error)
    ws.on_close(ws)

def on_close(ws):
    print("### closed ###")
    ws.close()

def on_open(ws):
    print("### open ###")
    contents = sendRequest(SYMBOL_LIST_ENDPOINT)
    symbols = getBitmexSymbolList(contents)
    ws.send(json.dumps(symbols))



def run(endpoint):
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(endpoint,
                                on_open = on_open,
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)

    ws.run_forever()

if __name__ == "__main__":
    run(ENDPOINT)