import json
import pymysql
import datetime
from website import sqlsetting
import json
# import sqlsetting

def orderlist_update():
    try:
        connection = sqlsetting.mysqlset()
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''select get_order from trade.get_order_list where userid = 1'''
        my_cursor.execute(sql)
        select_data = my_cursor.fetchone()
        connection.commit()
        connection.close()
        res = eval(select_data['get_order'])
        # res = json.loads(res)
        print(res[0])
    except Exception as e:
        print(e)
        print('bitmex_mysqldb.orderlist_update error')

orderlist_update()