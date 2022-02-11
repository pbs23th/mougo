import json
import pymysql
import datetime
from . import sqlsetting


def settingValue(user_id):
    try:
        connection = sqlsetting.mysqlset()
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''select * from trade.upbit_setting where userid = %s'''
        my_cursor.execute(sql, user_id)
        select_data = my_cursor.fetchone()
        connection.commit()
        connection.close()
        return select_data
    except Exception as e:
        print(e)
        print('upbit settingValue error')


def userValue(user_id):
    try:
        connection = sqlsetting.mysqlset()
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''select * from trade.user where id = %s'''
        my_cursor.execute(sql, user_id)
        select_data = my_cursor.fetchone()
        connection.commit()
        connection.close()
        return select_data
    except Exception as e:
        print(e)
        print('upbit userValue error')


def botStatus(user_id):
    try:
        connection = sqlsetting.mysqlset()
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''select * from trade.upbit_setting where userid = %s'''
        my_cursor.execute(sql, user_id)
        select_data = my_cursor.fetchone()
        connection.commit()
        connection.close()
        if select_data == None:
            return 400
        if select_data['botstatus'] == 0:
            data = 'off'
        else:
            data = 'on'
        return data
    except Exception as e:
        print(e)
        print('upbit botStatus error')

def botUpdate(user_id):
    try:
        connection = sqlsetting.mysqlset()
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''select * from trade.upbit_setting where userid = %s'''
        my_cursor.execute(sql, user_id)
        select_data = my_cursor.fetchone()

        if select_data['botstatus'] == 0:
            my_cursor = connection.cursor(pymysql.cursors.DictCursor)
            sql = '''update trade.upbit_setting set botstatus = 1 where userid = %s'''
            my_cursor.execute(sql, user_id)
            connection.commit()
            connection.close()

        else:
            my_cursor = connection.cursor(pymysql.cursors.DictCursor)
            sql = '''update trade.upbit_setting set botstatus = 0 where userid = %s'''
            my_cursor.execute(sql, user_id)
            connection.commit()
            connection.close()

        return
    except Exception as e:
        print(e)
        print('upbit botUpdate error')


def stoplossStatus(user_id):
    try:
        connection = sqlsetting.mysqlset()
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''select * from trade.upbit_setting where userid = %s'''
        my_cursor.execute(sql, user_id)
        select_data = my_cursor.fetchone()
        connection.commit()
        if select_data == None:
            return 400
        if select_data['stoploss_onoff'] == 0:
            data = 'off'
        else:
            data = 'on'
        connection.close()
        return data
    except Exception as e:
        print(e)
        print('upbit stoplossStatus error')

def stoplossUpdate(user_id):
    try:
        connection = sqlsetting.mysqlset()
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''select * from trade.upbit_setting where userid = %s'''
        my_cursor.execute(sql, user_id)
        select_data = my_cursor.fetchone()

        if select_data['stoploss_onoff'] == 0:
            my_cursor = connection.cursor(pymysql.cursors.DictCursor)
            sql = '''update trade.upbit_setting set stoploss_onoff = 1 where userid = %s'''
            my_cursor.execute(sql, user_id)
            connection.commit()
            connection.close()

        else:
            my_cursor = connection.cursor(pymysql.cursors.DictCursor)
            sql = '''update trade.upbit_setting set stoploss_onoff = 0 where userid = %s'''
            my_cursor.execute(sql, user_id)
            connection.commit()
            connection.close()
        return
    except Exception as e:
        print(e)
        print('upbit stoplossUpdate error')


def lastorder_update(price, market, user_id):
    try:
        connection = sqlsetting.mysqlset()
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''update trade.upbit_orderhistory set last_order = %s where market = %s and ordertype = 'price' and  userid = %s order by transact_time DESC limit 1'''
        my_cursor.execute(sql, (float(price), market, user_id))
        connection.commit()
        connection.close()
        return
    except Exception as e:
        print(e)
        print('upbit lastorder_update error')


def lastorder_select(market, user_id):
    try:
        connection = sqlsetting.mysqlset()
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''select * from trade.upbit_orderhistory where side = 'bid' and market = %s and ordertype = 'price' and userid = %s order by transact_time DESC limit 1'''
        my_cursor.execute(sql, (market, user_id))
        select_data = my_cursor.fetchone()
        connection.commit()
        connection.close()
        return select_data['last_order']
    except Exception as e:
        print(e)
        print('upbit lastorder_select error')


def buyintervalstatus(user_id):
    try:
        connection = sqlsetting.mysqlset()
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''select * from trade.upbit_buyintervalset where userid = %s'''
        my_cursor.execute(sql, user_id)
        select_data = my_cursor.fetchone()
        data = [select_data['buy_1'], select_data['buy_2'], select_data['buy_3'], select_data['buy_4'], select_data['buy_5'], select_data['buy_6'], select_data['buy_7'], select_data['buy_8'], select_data['buy_9']]
        connection.commit()
        connection.close()
        return data
    except Exception as e:
        print(e)
        print('upbit buyintervalstatus error')


def firstbuy_select(market, user_id):
    try:
        connection = sqlsetting.mysqlset()
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''select * from trade.upbit_orderhistory where market = %s and side = 'bid' and ordertype = 'price' and userid = %s order by  transact_time DESC limit 1 '''
        my_cursor.execute(sql, (market, user_id))
        select_data = my_cursor.fetchone()
        connection.commit()
        connection.close()
        return select_data['price']
    except Exception as e:
        print(e)
        print('upbit firstbuy_select error')




def appointmentStatus(user_id):
    try:
        connection = sqlsetting.mysqlset()
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''select * from trade.upbit_setting where userid = %s'''
        my_cursor.execute(sql, user_id)
        select_data = my_cursor.fetchone()
        connection.commit()
        if select_data == None:
            return 400
        if select_data['appointment'] == 0:
            data = 'off'
        else:
            data = 'on'
        connection.close()
        return data
    except Exception as e:
        print(e)
        print('upbit appointmentStatus error')


def appointmentUpdate(user_id):
    try:
        connection = sqlsetting.mysqlset()
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''select * from trade.upbit_setting where userid = %s'''
        my_cursor.execute(sql, user_id)
        select_data = my_cursor.fetchone()

        if select_data['appointment'] == 0:
            my_cursor = connection.cursor(pymysql.cursors.DictCursor)
            sql = '''update trade.upbit_setting set appointment = 1 where userid = %s'''
            my_cursor.execute(sql, user_id)
            connection.commit()
            connection.close()

        else:
            my_cursor = connection.cursor(pymysql.cursors.DictCursor)
            sql = '''update trade.upbit_setting set appointment = 0 where userid = %s'''
            my_cursor.execute(sql, user_id)
            connection.commit()
            connection.close()
        return
    except Exception as e:
        print(e)
        print('upbit appointmentUpdate error')


def botUpdate2(user_id):
    try:
        connection = sqlsetting.mysqlset()
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''update trade.upbit_setting set botstatus = 0, appointment = 0 where userid = %s'''
        my_cursor.execute(sql, user_id)
        connection.commit()
        connection.close()
        return
    except Exception as e:
        print(e)
        print('upbit botUpdate2 error')


def buyintervalStatus(user_id):
    try:
        connection = sqlsetting.mysqlset()
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''select * from trade.upbit_buyintervalset where userid = %s'''
        my_cursor.execute(sql, user_id)
        select_data = my_cursor.fetchone()
        connection.commit()
        connection.close()
        return select_data
    except Exception as e:
        print(e)
        print('upbit buyintervalStatus error')



def select_orddata(data, user_id):
    try:
        ''' 누적수익, 거래량 가져오기 '''
        connection = sqlsetting.mysqlset()
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''select * from trade.upbit_orderhistory where market = %s and userid= %s'''
        my_cursor.execute(sql, (data, user_id))
        select_data = my_cursor.fetchall()
        connection.commit()
        connection.close()
        select_data = sorted(select_data, key=lambda person: (person['transact_time']), reverse=True)
        # print(select_data)
        buy_price = 0
        buy_valume = 0
        sell_price = 0
        sell_valume = 0
        buy_fee = 0
        sell_fee = 0
        realbuy = 0
        realvol = 0
        realsell = 0
        count = 0
        if len(select_data) > 0:
            for i in select_data:
                if select_data[0]['side'] == 'ask' and i['remaining_volume'] == (0 or None):
                    break

                if i['side'] == 'bid':
                    realbuy += float(i['price']) * float(i['unit'])  # 체결가격
                    realvol += float(i['unit'])  # 체결수량
                    if i['ordertype'] == 'price':
                        del select_data[0:count+1]
                        break
                elif i['side'] == 'ask' and i['remaining_volume'] > 0:
                    realsell += float(i['price']) * float(i['unit'])
                else:
                    break
                count += 1
            count2 = 0
            for i in select_data:
                if i['side'] == 'bid':
                    buy_price += float(i['price']) * float(i['unit'])  # 체결가격
                    buy_valume += float(i['unit'])  # 체결수량
                    buy_fee += float(i['fee'])  # 수수료
                    count2 += 1
                else:
                    sell_price += float(i['price']) * float(i['unit'])  # 체결가격
                    sell_valume += float(i['unit'])  # 체결수량
                    sell_fee += float(i['fee'])  # 수수료
        if buy_valume != 0 and sell_valume != 0:
            trade_vol = sell_price + buy_price + realbuy + realsell
            trade_vol2 = sell_price - buy_price
            data = trade_vol2 - sell_fee - buy_fee
            return data, trade_vol
        else:
            return 0, 0
    except Exception as e:
        print(e)
        print('upbit_-select_orddata error')
        return 0, 0

#

def insert_data(getorder, user_id):
    try:
        ''' 거래내역 저장 '''
        connection = sqlsetting.mysqlset()
        if len(getorder) > 0:
            for i in getorder:
                print(i)
                order_time = datetime.datetime.strptime(i['created_at'][:-6],'%Y-%m-%dT%H:%M:%S')
                transact_time = None
                market = i['market']
                ordId = i['uuid']
                side = i['side']
                unit = 0
                funds = 0
                fee = i['paid_fee']
                ordertype = i['ord_type']
                remaining_volume = i['remaining_volume']
                if len(i['trades']) > 0:
                    for j in i['trades']:
                        funds += float(j['funds'])
                        unit += float(j['volume'])
                        if i['trades'][-1] == j:
                            transact_time = datetime.datetime.strptime(j['created_at'][:-6],'%Y-%m-%dT%H:%M:%S')
                    price = funds/unit
                    my_cursor = connection.cursor(pymysql.cursors.DictCursor)
                    sql = '''insert into trade.upbit_orderhistory(order_time, market, side, price, unit, fee, ordertype, transact_time, userid, ordId, remaining_volume, last_order) 
                    SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 0 FROM dual where not exists(select ordId from trade.upbit_orderhistory where ordId = %s and userid = %s)'''
                    my_cursor.execute(sql,(order_time, market, side, price, unit, fee, ordertype, transact_time, user_id, ordId, remaining_volume, ordId, user_id))
                connection.commit()
            connection.close()
            return
    except Exception as e:
        print(e)
        print('upbit_insert_data : error')



def insert_ordid(getorder, user_id):
    try:
        ''' 주문내역 저장 '''
        connection = sqlsetting.mysqlset()
        time = datetime.datetime.strptime(getorder['created_at'][:-6],'%Y-%m-%dT%H:%M:%S')
        market = getorder['market']
        ordId = getorder['uuid']
        state = '1'
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''insert into trade.upbit_ordidlist(time, market, ordId, userid, state) 
        SELECT %s, %s, %s, %s, %s FROM dual where not exists(select ordId from trade.upbit_ordidlist where ordId = %s and userid = %s)'''
        my_cursor.execute(sql,(time, market, ordId, user_id, state , ordId, user_id))
        connection.commit()
        connection.close()
        return
    except Exception as e:
        print(e)
        print('mysqlddb.insert_ordid error')



def select_ordid(marketid, userid):
    try:
        ''' 주문내역 가져오기 '''
        connection = sqlsetting.mysqlset()
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''select * from trade.upbit_ordidlist where market = %s and userid = %s and state = %s '''
        my_cursor.execute(sql, (marketid, userid, str(1)))
        select_data = my_cursor.fetchall()
        connection.commit()
        connection.close()
        return select_data
    except Exception as e:
        print(e)
        print('upbit_mysqlddb.select_ordid error')



def update_ordid(data, status):
    try:
        ''' 주문내역 업데이트 '''
        connection = sqlsetting.mysqlset()
        for i in data:
            state = status
            ordId = i['uuid']
            my_cursor = connection.cursor(pymysql.cursors.DictCursor)
            sql = '''update trade.upbit_ordidlist set state = %s where ordId = %s'''
            my_cursor.execute(sql, (state, ordId))
            connection.commit()
        connection.close()
        return
    except Exception as e:
        print(e)
        print('mysqlddb.update_ordid error')