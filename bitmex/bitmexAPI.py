import requests
import time
import hmac
import hashlib
import json


class Bitmex:

    base_url = 'https://testnet.bitmex.com'

    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret



    def bitmex_my_position(self, currency='XBt'):
        try:
            data = {'filter': {"currency": currency}}
            verb = 'GET'
            function_url = '/api/v1/position'
            url = self.base_url + function_url
            expires = int(round(time.time()) + 5)
            message = verb + function_url + str(expires) + json.dumps(data)
            signature = hmac.new(bytes(self.api_secret, 'utf-8'), bytes(message, 'utf-8'),
                                 digestmod=hashlib.sha256).hexdigest()
            headers = {'api-expires': str(expires), 'api-key': self.api_key, 'api-signature': signature}
            r = requests.get(url, headers=headers, json=data)

        except:
            pass

        return r.text




    def cancel_order(self, orderID ='orderID'):
        try:
            data = {"orderID": orderID}
            verb = 'DELETE'
            function_url = '/api/v1/order'
            url = self.base_url + function_url
            expires = int(round(time.time()) + 5)
            message = verb + function_url + str(expires) + json.dumps(data)
            signature = hmac.new(bytes(self.api_secret, 'utf-8'), bytes(message, 'utf-8'),
                                 digestmod=hashlib.sha256).hexdigest()
            headers = {'api-expires': str(expires), 'api-key': self.api_key, 'api-signature': signature}
            r = requests.delete(url, headers=headers, json=data)
        except:
            pass
        return r.text





    def buy_order(self, limit_price=100, symbol='XBTUSD', ordtype='limit', buysell_side='Buy', orderQty=1):

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
            expires = int(round(time.time()) + 5)
            message = verb + function_url + str(expires) + json.dumps(data)
            signature = hmac.new(bytes(self.api_secret, 'utf-8'), bytes(message, 'utf-8'),
                                 digestmod=hashlib.sha256).hexdigest()
            headers = {'api-expires': str(expires), 'api-key': self.api_key, 'api-signature': signature}
            r = requests.post(url, headers=headers, json=data)

            # rr = r.text
            #
            # json.dumps(rr)
            # b = json.loads()
            # print(b)
        except:
            print('error')
        return r.text




    def sell_order(self, limit_price=100000, symbol='XBTUSD', ordtype='limit', buysell_side='Sell', orderQty=1):
    # success_tf = False
    # while not success_tf:
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
        expires = int(round(time.time()) + 5)
        message = verb + function_url + str(expires) + json.dumps(data)
        signature = hmac.new(bytes(self.api_secret, 'utf-8'), bytes(message, 'utf-8'),
                             digestmod=hashlib.sha256).hexdigest()
        headers = {'api-expires': str(expires), 'api-key': self.api_key, 'api-signature': signature}
        r = requests.post(url, headers=headers, json=data)

        return r.text





    def bitmex_my_balance(self, currency='XBt'):
        print('---------------------------------------')
        data = {'currency': currency}
        verb = 'GET'
        function_url = '/api/v1/user/margin'
        url = self.base_url + function_url
        expires = int(round(time.time()) + 5)
        message = verb + function_url + str(expires) + json.dumps(data)
        signature = hmac.new(bytes(self.api_secret, 'utf-8'), bytes(message, 'utf-8'),
                             digestmod=hashlib.sha256).hexdigest()
        headers = {'api-expires': str(expires), 'api-key': self.api_key, 'api-signature': signature}
        r = requests.get(url, headers=headers, json=data)
        a = r.text
        return a



    def open_order(self, symbol='XBt'):
        data = {'currency' : symbol, 'filter' : {"open": True}}
        verb = 'GET'
        function_url = '/api/v1/order'
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

        return r.text