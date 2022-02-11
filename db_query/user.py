import json
import pymysql
import datetime
# import website.sqlsetting as sqlsetting
from website import sqlsetting


def user(user_id):
    try:
        connection = sqlsetting.mysqlset()
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''select * from trade.user where id = %s'''
        my_cursor.execute(sql, user_id)
        res = my_cursor.fetchone()
        connection.commit()
        connection.close()
        return res
    except Exception as e:
        return None


def api_key(user_id):
    try:
        connection = sqlsetting.mysqlset()
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''select * from trade.api_key where user_id = %s'''
        my_cursor.execute(sql, user_id)
        res = my_cursor.fetchall()
        connection.commit()
        connection.close()
        return res
    except Exception as e:
        return None


def update_api_key(number):
    try:
        connection = sqlsetting.mysqlset()
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''delete from trade.api_key where id = %s'''
        my_cursor.execute(sql, number)
        connection.commit()
        connection.close()
        return True
    except Exception as e:
        return None


def insert_api_key(user_id,  exchange, accessKey, secretKey,passphrase='0'):
    try:
        connection = sqlsetting.mysqlset()
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''insert into trade.api_key(user_id, exchange, access_key, secret_key, passphrase) value(%s, %s, %s, %s, %s)'''
        my_cursor.execute(sql, (user_id,exchange, accessKey, secretKey, passphrase))
        connection.commit()
        connection.close()
        return 'seccess'
    except Exception as e:
        return None


def select_api_key(user_id):
    try:
        connection = sqlsetting.mysqlset()
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''select * from trade.api_key where user_id = %s '''
        my_cursor.execute(sql, (user_id))
        res = my_cursor.fetchall()
        connection.commit()
        connection.close()
        print(res)
        return res
    except Exception as e:
        return None



def insert_user_data(data):
    exchange = data['exchange']
    start_payment = 1000
    botstatus = 0
    count = 5
    positionsell = 0.5
    loss_stop = 0
    stoploss_onoff = 0
    appointment = 0
    entry_position = 'long'
    bot_id = data['id']
    if exchange == 'UPBIT':
        currency = 'BTC'
        payment = 'KRW'

    elif exchange == 'OKEX':
        currency = 'BTC'
        payment = 'USDT'

    else:
        currency = 'XBTUSD'
        payment = 'XBT'
    connection = sqlsetting.mysqlset()
    my_cursor = connection.cursor(pymysql.cursors.DictCursor)
    sql = '''insert into trade.buyintervalset(buy_1,buy_2,buy_3,buy_4,buy_5,buy_6,buy_7,buy_8,buy_9, bot_id) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
    my_cursor.execute(sql, (0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3, bot_id))
    connection.commit()

    my_cursor = connection.cursor(pymysql.cursors.DictCursor)
    sql = '''insert into trade.bot_setting(start_payment,currency,botstatus,count,positionsell,payment, entry_position, loss_stop, stoploss_onoff, appointment, bot_id) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
    my_cursor.execute(sql, (start_payment, currency, botstatus, count, positionsell, payment, entry_position, loss_stop, stoploss_onoff, appointment, bot_id))
    connection.commit()
    connection.close()
    return 200


def select_bot_setting(bot_id):
    connection = sqlsetting.mysqlset()
    my_cursor = connection.cursor(pymysql.cursors.DictCursor)
    sql = '''select * from trade.bot_setting where bot_id = %s '''
    my_cursor.execute(sql, bot_id)
    res = my_cursor.fetchone()
    connection.commit()
    connection.close()
    return res


def buyintervalStatus(bot_id):
    connection = sqlsetting.mysqlset()
    my_cursor = connection.cursor(pymysql.cursors.DictCursor)
    sql = '''select * from trade.buyintervalset where bot_id = %s'''
    my_cursor.execute(sql, bot_id)
    select_data = my_cursor.fetchone()
    connection.commit()
    connection.close()
    return select_data
