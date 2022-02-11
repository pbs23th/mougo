import okex.Public_api as public
import json
import pymysql
import datetime

def insert():
    api_key = '1a0fef19-d4b7-4f1a-adc8-5d4466f2a9b2'
    secret_key = '3D54ADBDA45C14057440333B7F52E82C'
    passphrase = '0150590'
    flag = '0'
    publicAPI = public.PublicAPI(api_key, secret_key, passphrase, False, flag)
    a = publicAPI.get_instruments(instType='SPOT')
    print(a.text.headers)
    # aa = a['data']
    # connection = pymysql.connect(
    #     user='gmc',
    #     port=3306,
    #     passwd='Gmc1234!',
    #     host='127.0.0.1',
    #     db='trade',
    #     charset='utf8'
    # )
    # for a in aa:
    #     print(a)
    #     baseCcy = a['baseCcy']
    #     category = a['category']
    #     instId = a['instId']
    #     instType = a['instType']
    #     lever = a['lever']
    #     listTime = a['listTime']
    #     lotSz = a['lotSz']
    #     minSz = a['minSz']
    #     quoteCcy = a['quoteCcy']
    #     state = a['state']
    #     tickSz = a['tickSz']
    #
    #
    #     my_cursor = connection.cursor(pymysql.cursors.DictCursor)
    #     sql = '''insert into trade.okex_instrument(baseCcy, category, instId, instType, lever, listTime, lotSz, minSz, quoteCcy, state, tickSz) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
    #     my_cursor.execute(sql, (baseCcy, category, instId, instType, lever, listTime, lotSz, minSz, quoteCcy, state, tickSz))
    #     connection.commit()
    # connection.close()
# (instType, instId, uly, category, baseCcy, quoteCcy, settleCcy, ctVal, ctMult, ,ctValCcy, optType, stk, listTime, expTime, lever, tickSz, lotSz, minSz, ctType, alias, state)

insert()