import requests
import time
import hmac
import hashlib
import json
import datetime


class Bitmex:

    base_url = 'https://www.bitmex.com'

    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret



    def signature(self, verb, function_url, data):
        verb = verb
        expires = int(round(time.time()) + 5)
        message = verb + function_url + str(expires) + json.dumps(data)
        signature = hmac.new(bytes(self.api_secret, 'utf-8'), bytes(message, 'utf-8'),
                             digestmod=hashlib.sha256).hexdigest()
        headers = {'api-expires': str(expires), 'api-key': self.api_key, 'api-signature': signature}
        return headers



    def bitmex_my_balance(self, symbol='XBTUSD'):
        data = {'symbol': symbol}
        verb = 'GET'
        function_url = '/api/v1/user/margin'
        url = self.base_url + function_url
        headers = self.signature(verb, function_url, data)
        r = requests.get(url, headers=headers, json=data)
        test = r.headers
        if 'x-ratelimit-remaining' in test:
            print('=====================bitmex_my_balance',test['x-ratelimit-remaining'])
        else:
            print('=====================bitmex_my_balance : ')
        a = r.json()
        return a



    def bitmex_my_position(self, symbol='XBTUSD'):
        try:
            data = {'filter': {"symbol": symbol}}

            verb = 'GET'
            function_url = '/api/v1/position'
            url = self.base_url + function_url
            headers = self.signature(verb, function_url, data)
            r = requests.get(url, headers=headers, json=data)
            a = r.json()
            if len(a) > 0:
                data = []
                for i in a:
                    if i['symbol'] == symbol:
                        data.append(i)
                return data[0]
            else:
                print('None data')
                return None

        except:
            return None



    # def get_ticker(self, symbol='XBTUSD'):
    #     try:
    #         print('-------------------get-ticker')
    #         data = {'filter': {"symbol": symbol},
    #                            "count" : 1,
    #                            "reverse" : "true"}
    #         function_url = '/api/v1/trade'
    #         url = self.base_url + function_url
    #         r = requests.get(url, json=data)
    #         aa = r.headers
    #         a = r.json()
    #         data = a[0]['price']
    #         return data
    #     except:
    #         print('error---------')
    #         pass
    #
    #     return data



    def cancel_order(self, orderID ='orderID'):
        try:
            data = {"orderID": orderID}
            verb = 'DELETE'
            function_url = '/api/v1/order'
            url = self.base_url + function_url
            headers = self.signature(verb, function_url, data)
            r = requests.delete(url, headers=headers, json=data)
        except:
            pass
        return r.json()


    def cancel_all(self, symbol ='XBTUSD', side='Buy'):
        try:
            data = {'filter': {"side": side},
                    'symbol' : symbol }
            verb = 'DELETE'
            function_url = '/api/v1/order/all'
            url = self.base_url + function_url
            headers = self.signature(verb, function_url, data)
            r = requests.delete(url, headers=headers, json=data)
            print('cancel order---------------------')
            print('cancel : ', r.sjon())
        except:
            pass
        return r.json()


    def bitmex_order(self, limit_price=None, symbol='XBTUSD', ordtype='limit', buysell_side='Buy', orderQty=None):

        try:
            if ordtype == 'limit':
                data = {'symbol': symbol,
                        'orderQty': orderQty,
                        'price': limit_price,
                        'side': buysell_side,
                        'ordType': 'Limit'}
            elif ordtype == 'market':
                data = {'symbol': symbol,
                        'orderQty': orderQty,
                        'side': buysell_side,
                        'ordType': 'Market'}
            else:
                print('data error occurred')
                return 0
            verb = 'POST'
            function_url = '/api/v1/order'
            url = self.base_url + function_url
            headers = self.signature(verb, function_url, data)
            r2 = requests.post(url, headers=headers, json=data)
        except:
            print('error')
        return r2.json()



    def open_order(self, symbol='XBTUSD'):
        data = {'symbol' : symbol, 'filter' : {"open": True}}
        verb = 'GET'
        function_url = '/api/v1/order'
        url = self.base_url + function_url
        headers = self.signature(verb, function_url, data)
        r = requests.get(url, headers=headers, json=data)
        test = r.headers
        # print('open_order-------------------------------------------------')
        # print(test)
        # print('-------------------------------------------------')
        return r.json()


    def order_history(self, symbol='XBTUSD'):
        data = {'symbol' : symbol ,'count' : 10, 'reverse' : 'true'}
        verb = 'GET'
        function_url = '/api/v1/order'
        url = self.base_url + function_url
        headers = self.signature(verb, function_url, data)
        r = requests.get(url, headers=headers, json=data)
        a = r.json()
        # print(a)
        return a


    def get_order(self, orderID = 'd655d409-590b-4c73-96b5-ca67f139cc54'):
        data = {'filter' : {'orderID' : orderID}}
        verb = 'GET'
        function_url = '/api/v1/order'
        url = self.base_url + function_url
        headers = self.signature(verb, function_url, data)
        r = requests.get(url, headers=headers, json=data)
        a = r.json()
        # print(a)
        return a


    def ohlc(self, binSize = '1h', symbol = 'XBTUSD', count = 100, reverse = True):
        data = {'binSize' : binSize, 'symbol' : symbol, 'count' : count, 'reverse' : reverse}
        verb = 'GET'
        function_url = '/api/v1/trade/bucketed'
        url = self.base_url + function_url
        expires = int(round(time.time()) + 5)
        message = verb + function_url + str(expires) + json.dumps(data)
        signature = hmac.new(bytes(self.api_secret, 'utf-8'), bytes(message, 'utf-8'),
                             digestmod=hashlib.sha256).hexdigest()
        headers = {'api-expires': str(expires), 'api-key': self.api_key, 'api-signature': signature}
        r = requests.get(url, headers=headers, json=data)
        a = r.text
        # print(a)
        return a



    def position_close(self, symbol='XBTUSD'):
        data = {'symbol' : symbol}
        verb = 'POST'
        function_url = '/api/v1/order/closePosition'
        url = self.base_url + function_url
        expires = int(round(time.time()) + 5)
        message = verb + function_url + str(expires) + json.dumps(data)
        signature = hmac.new(bytes(self.api_secret, 'utf-8'), bytes(message, 'utf-8'),
                             digestmod=hashlib.sha256).hexdigest()
        headers = {'api-expires': str(expires), 'api-key': self.api_key, 'api-signature': signature}
        r = requests.post(url, headers=headers, json=data)

        return r.json()