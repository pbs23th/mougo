import json
import pymysql
import datetime
from . import sqlsetting


def settingValue(user_id):
    try:
        ''' 셋팅값 가져오기'''
        connection = sqlsetting.mysqlset()
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''select * from trade.okex_setting where userid = %s'''
        my_cursor.execute(sql, user_id)
        select_data = my_cursor.fetchone()
        connection.commit()
        connection.close()
        return select_data
    except Exception as e:
        print(e)
        print('mysqlddb.settingValue error')


def userValue(user_id):
    try:
        ''' 로그인한 유저정보 가져오기'''
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
        print('mysqlddb.userValue error')


def botStatus(user_id):
    try:
        ''' 봇 상태값 가져오기'''
        connection = sqlsetting.mysqlset()
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''select * from trade.okex_setting where userid = %s'''
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
        print('mysqlddb.botStatus error')

def botUpdate(user_id):
    try:
        ''' 봇 상태 업데이트 '''
        connection = sqlsetting.mysqlset()
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''select * from trade.okex_setting where userid = %s'''
        my_cursor.execute(sql, user_id)
        select_data = my_cursor.fetchone()

        if select_data['botstatus'] == 0:
            my_cursor = connection.cursor(pymysql.cursors.DictCursor)
            sql = '''update trade.okex_setting set botstatus = 1 where userid = %s'''
            my_cursor.execute(sql, user_id)
            connection.commit()
            connection.close()

        else:
            my_cursor = connection.cursor(pymysql.cursors.DictCursor)
            sql = '''update trade.okex_setting set botstatus = 0 where userid = %s'''
            my_cursor.execute(sql, user_id)
            connection.commit()
            connection.close()
        return 200
    except Exception as e:
        print(e)
        print('mysqlddb.botUpdate error')


def stoplossStatus(user_id):
    try:
        ''' 스탑로스 상태값 가져오기 '''
        connection = sqlsetting.mysqlset()
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''select * from trade.okex_setting where userid = %s'''
        my_cursor.execute(sql, user_id)
        select_data = my_cursor.fetchone()
        connection.commit()
        connection.close()
        if select_data == None:
            return 400
        if select_data['stoploss_onoff'] == 0:
            data = 'off'
        else:
            data = 'on'
        return data
    except Exception as e:
        print(e)
        print('mysqlddb.stoplossStatus error')


def stoplossUpdate(user_id):
    try:
        ''' 스탑로스 상태값 업데이트 '''
        connection = sqlsetting.mysqlset()
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''select * from trade.okex_setting where userid = %s'''
        my_cursor.execute(sql, user_id)
        select_data = my_cursor.fetchone()

        if select_data['stoploss_onoff'] == 0:
            my_cursor = connection.cursor(pymysql.cursors.DictCursor)
            sql = '''update trade.okex_setting set stoploss_onoff = 1 where userid = %s'''
            my_cursor.execute(sql, user_id)
            connection.commit()
            connection.close()

        else:
            my_cursor = connection.cursor(pymysql.cursors.DictCursor)
            sql = '''update trade.okex_setting set stoploss_onoff = 0 where userid = %s'''
            my_cursor.execute(sql, user_id)
            connection.commit()
            connection.close()
        return
    except Exception as e:
        print(e)
        print('mysqlddb.stoplossUpdate error')


def lastorder_update(price, market, user_id):
    try:
        ''' 마지막 물타기 주문가격 업데이트'''
        connection = sqlsetting.mysqlset()
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''update trade.okex_orderhistory set last_order = %s where market = %s and ordertype = 'market' and  userid = %s order by transact_time DESC limit 1'''
        my_cursor.execute(sql, (float(price), market, user_id))
        connection.commit()
        connection.close()
        return
    except Exception as e:
        print(e)
        print('mysqlddb.lastorder_update error')


def lastorder_select(market, user_id):
    try:
        ''' 마지막 물타기 주문가격 가져오기'''
        connection = sqlsetting.mysqlset()
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''select * from trade.okex_orderhistory where side = 'buy' and market = %s and ordertype = 'market' and userid = %s order by transact_time DESC limit 1'''
        my_cursor.execute(sql, (market, user_id))
        select_data = my_cursor.fetchone()
        connection.commit()
        connection.close()
        return select_data['last_order']
    except Exception as e:
        print(e)
        print('mysqlddb.lastorder_select error')



def firstbuy_select(market, user_id):
    try:
        ''' 최초 주문가격 가져오기 '''
        connection = sqlsetting.mysqlset()
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''select * from trade.okex_orderhistory where market = %s and side = 'buy' and ordertype = 'market'  and userid = %s order by  transact_time DESC limit 1 '''
        my_cursor.execute(sql, (market, user_id))
        select_data = my_cursor.fetchone()
        connection.commit()
        connection.close()
        return select_data['price']
    except Exception as e:
        print(e)
        print('mysqlddb.firstbuy_select error')



def appointmentStatus(user_id):
    try:
        ''' 오프 예약 상태값 가져오기 '''
        connection = sqlsetting.mysqlset()
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''select * from trade.okex_setting where userid = %s'''
        my_cursor.execute(sql, user_id)
        select_data = my_cursor.fetchone()
        connection.commit()
        connection.close()
        if select_data == None:
            return 400
        if select_data['appointment'] == 0:
            data = 'off'
        else:
            data = 'on'
        return data
    except Exception as e:
        print(e)
        print('mysqlddb.appointmentStatus error')


def appointmentUpdate(user_id):
    try:
        ''' 오프예약 상태값 업데이트'''
        connection = sqlsetting.mysqlset()
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''select * from trade.okex_setting where userid = %s'''
        my_cursor.execute(sql, user_id)
        select_data = my_cursor.fetchone()

        if select_data['appointment'] == 0:
            my_cursor = connection.cursor(pymysql.cursors.DictCursor)
            sql = '''update trade.okex_setting set appointment = 1 where userid = %s'''
            my_cursor.execute(sql, user_id)
            connection.commit()
            connection.close()

        else:
            my_cursor = connection.cursor(pymysql.cursors.DictCursor)
            sql = '''update trade.okex_setting set appointment = 0 where userid = %s'''
            my_cursor.execute(sql, user_id)
            connection.commit()
            connection.close()
        return
    except Exception as e:
        print(e)
        print('mysqlddb.appointmentUpdate error')


def botUpdate2(user_id):
    try:
        ''' 오프예약 발동시 봇상태 예약상태 모두 오프변경 '''
        connection = sqlsetting.mysqlset()
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''update trade.okex_setting set botstatus = 0, appointment = 0 where userid = %s'''
        my_cursor.execute(sql, user_id)
        connection.commit()
        connection.close()
        return
    except Exception as e:
        print(e)
        print('mysqlddb.botUpdate2 error')



def buyintervalstatus(user_id):
    try:
        ''' 추가매수 간격 가져오기'''
        connection = sqlsetting.mysqlset()
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''select * from trade.okex_buyintervalset where userid = %s'''
        my_cursor.execute(sql, user_id)
        select_data = my_cursor.fetchone()
        connection.commit()
        connection.close()
        data = [select_data['buy_1'], select_data['buy_2'], select_data['buy_3'], select_data['buy_4'], select_data['buy_5'], select_data['buy_6'], select_data['buy_7'], select_data['buy_8'], select_data['buy_9']]
        return data
    except Exception as e:
        print(e)
        print('mysqlddb.buyintervalstatus error')


def buyintervalStatus(user_id):
    try:
        connection = sqlsetting.mysqlset()
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''select * from trade.okex_buyintervalset where userid = %s'''
        my_cursor.execute(sql, user_id)
        select_data = my_cursor.fetchone()
        connection.commit()
        connection.close()
        return select_data
    except Exception as e:
        print(e)
        print('mysqlddb.buyintervalStatus error')


def select_orddata(data, user_id):
    try:
        ''' 누적수익, 거래량 가져오기 '''
        connection = sqlsetting.mysqlset()
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''select * from trade.okex_orderhistory where market = %s and userid= %s'''
        my_cursor.execute(sql, (data, user_id))
        select_data = my_cursor.fetchall()
        # print(select_data)
        connection.commit()
        connection.close()
        select_data = sorted(select_data, key=lambda person: (person['transact_time']), reverse=True)
        # print(select_data)
        buy_price = 0
        buy_valume = 0
        sell_price = 0
        sell_valume = 0
        sell_fee = 0
        realbuy = 0
        realvol = 0
        realsell = 0
        count = 0
        avglen = []
        if len(select_data) > 0:
            for i in select_data:
                if i['side'] == 'sell' and i['state'] == 'limit':
                    break

                if i['side'] == 'buy':
                    realbuy += float(i['price']) * float(i['unit'])
                    realvol += float(i['unit'])  # 체결수량
                    avglen.append(i['side'])
                    if i['ordertype'] == 'market':
                        del select_data[0:count+1]
                        break

                elif i['side'] == 'sell' and i['state'] == 'canceled':
                    realsell = float(i['price']) * float(i['unit'])

                else:
                    break

                count += 1
            count2 = 0
            for i in select_data:
                if i['side'] == 'buy':
                    buy_price += float(i['price']) * float(i['unit'])  # 체결가격
                    buy_valume += float(i['unit'])  # 체결수량
                    # buy_fee += float(i['fee']) # 수수료
                    count2 += 1
                else:
                    sell_price += float(i['price']) * float(i['unit'])  # 체결가격
                    sell_valume += float(i['unit'])  # 체결수량
                    sell_fee += float(i['fee'])  # 수수료
            trade_vol = sell_price + buy_price + realbuy + realsell
            trade_vol2 = sell_price - buy_price
            data = trade_vol2 + sell_fee
            if len(avglen) > 0:
                print('sdfsdfsdfsfsfs')
                avgprice = realbuy / realvol
                print(avgprice)
            else:
                print('1111111111111111sdfsdfsdfsfsfs')
                avgprice = 0
                print(avgprice)

            return data, trade_vol, avgprice
        else:
            return 0, 0, 0
    except Exception as e:
        print(e)
        print('okex_select_orddata error')
        return 0, 0, 0


def insert_data(getorder, user_id):
    try:
        ''' 거래내역 저장 '''
        connection = sqlsetting.mysqlset()
        if len(getorder) > 0:
            for i in getorder:
                order_time = datetime.datetime.utcfromtimestamp(int(i['cTime'][:10]))+datetime.timedelta(hours=9)
                transact_time = datetime.datetime.utcfromtimestamp(int(i['uTime'][:10]))+datetime.timedelta(hours=9)
                market = i['instId']
                ordId = i['ordId']
                side = i['side']
                price = i['avgPx']
                unit = i['accFillSz']
                fee = i['fee']
                ordertype = i['ordType']

                my_cursor = connection.cursor(pymysql.cursors.DictCursor)
                sql = '''insert into trade.okex_orderhistory(order_time, market, ordId, side, price, unit, fee, ordertype, transact_time, userid, last_order) 
                SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 0 FROM dual where not exists(select ordId from trade.okex_orderhistory where ordId = %s and userid = %s)'''
                my_cursor.execute(sql,(order_time, market, ordId, side, price, unit, fee, ordertype, transact_time, user_id, ordId, user_id))
                connection.commit()
            connection.close()
            return 200
    except Exception as e:
        print(e)
        print('insert_data : error')


def insert_ordid(getorder, user_id):
    try:
        ''' 주문내역 저장 '''
        connection = sqlsetting.mysqlset()
        time = datetime.datetime.utcfromtimestamp(int(getorder['cTime'][:10]))+datetime.timedelta(hours=9)
        market = getorder['instId']
        ordId = getorder['ordId']
        state = '1'
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''insert into trade.okex_ordidlist(time, market, ordId, userid, state) 
        SELECT %s, %s, %s, %s, %s FROM dual where not exists(select ordId from trade.okex_ordidlist where ordId = %s and userid = %s)'''
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
        sql = '''select * from trade.okex_ordidlist where market = %s and userid = %s and state = %s '''
        my_cursor.execute(sql, (marketid, userid, str(1)))
        select_data = my_cursor.fetchall()
        connection.commit()
        connection.close()
        return select_data
    except Exception as e:
        print(e)
        print('okex_mysqlddb.select_ordid error')


def update_ordid(data, status):
    try:
        ''' 주문내역 업데이트 '''
        connection = sqlsetting.mysqlset()
        for i in data:
            if status == 'not_exist':
                state2 = 'not_exist'
            else:
                state2 = i['state']
            ordId = i['ordId']
            my_cursor = connection.cursor(pymysql.cursors.DictCursor)
            sql = '''update trade.okex_ordidlist set state = %s where ordId = %s'''
            my_cursor.execute(sql, (state2, ordId))
            connection.commit()
        connection.close()
        return
    except Exception as e:
        print(e)
        print('mysqlddb.update_ordid error')


def min_sz(marketid):
    try:
        ''' 호가단위, 주문자릿수, 최소주문수량 가져오기 '''
        connection = sqlsetting.mysqlset()
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''select * from trade.okex_instrument where instId = %s'''
        my_cursor.execute(sql,marketid)
        select_data = my_cursor.fetchone()
        connection.commit()
        connection.close()
        return {
                'minSz' : select_data['minSz'],
                'stepprice' : select_data['tickSz'],
                'unitformat' : select_data['lotSz']
        }
    except Exception as e:
        print(e)
        print('mysqlddb.min_sz error')