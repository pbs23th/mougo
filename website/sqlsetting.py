import json
import pymysql
import datetime

def mysqlset():
    try:
        ''' 셋팅값 가져오기'''
        connection = pymysql.connect(
            user='root',
            port=3306,
            passwd='root',
            host='127.0.0.1',
            db='trade',
            charset='utf8'
        )
        return connection
    except Exception as e:
        print(e)
        print('mysqlset error')