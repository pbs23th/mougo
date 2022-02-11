import time
import requests
import bitmexAPI
# import bitmexAPI
# import bitmex_mysqldb



class test:
    def __init__(self):
        self.user_id = '1'
        api_key = 'A-_pfXq9ech1iAnUCWhZWOA9'
        secret_key = 'fKdiH4mpq2v0ITu5Dol_QojTS__oxxL8fJQ9I8qVwEWeV1Ag'
        self.bitmex = bitmexAPI.Bitmex(api_key, secret_key)


    def order_such(self):
        order_id = 'f77b9160-cb8d-4910-8af8-3df200e688f2'
        res = self.bitmex.get_order(order_id)
        print(res)
        return

test().order_such()