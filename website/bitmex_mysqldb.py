import json
import pymysql
import datetime
from . import sqlsetting
# import sqlsetting


def avg_update(data, userid):
    try:
        connection = sqlsetting.mysqlset()
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''INSERT INTO trade.gat_avg (gat_avg_data, userid) VALUES (%s, %s) ON DUPLICATE KEY UPDATE gat_avg_data=%s'''
        my_cursor.execute(sql, (str(data), userid, str(data)))
        connection.commit()
        connection.close()
    except Exception as e:
        print(e)
        print('bitmex_mysqldb.avg_update error')


def avg_select(userid):
    try:
        connection = sqlsetting.mysqlset()
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''select gat_avg_data from trade.gat_avg where userid = %s'''
        my_cursor.execute(sql, userid)
        select_data = my_cursor.fetchone()
        connection.commit()
        connection.close()
        if select_data is None:
            pass
            return [0,0]
        else:
            res = eval(select_data['gat_avg_data'])
            return res
    except Exception as e:
        print(e)
        print('bitmex_mysqldb.avg_select error')
        return [0, 0]


def balance_update(data, userid):
    try:
        connection = sqlsetting.mysqlset()
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''INSERT INTO trade.balance (balance, userid) VALUES (%s, %s) ON DUPLICATE KEY UPDATE balance=%s'''
        my_cursor.execute(sql, (float(data), userid, float(data)))
        connection.commit()
        connection.close()
    except Exception as e:
        print(e)
        print('bitmex_mysqldb.balance_update error')


def wallet_update(data, userid):
    try:
        connection = sqlsetting.mysqlset()
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''INSERT INTO trade.wallet_balance (wallet_balance, userid) VALUES (%s, %s) ON DUPLICATE KEY UPDATE wallet_balance=%s'''
        my_cursor.execute(sql, (float(data), userid, float(data)))
        connection.commit()
        connection.close()
    except Exception as e:
        print(e)
        print('bitmex_mysqldb.balance_update error')


def balance_select(userid):
    try:
        connection = sqlsetting.mysqlset()
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''select balance from trade.balance where userid = %s'''
        my_cursor.execute(sql, userid)
        select_data = my_cursor.fetchone()
        connection.commit()
        connection.close()
        res = select_data['balance']
        return res
    except Exception as e:
        print(e)
        print('bitmex_mysqldb.balance_select error')
        return 0


def wallet_select(userid):
    try:
        connection = sqlsetting.mysqlset()
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''select wallet_balance from trade.wallet_balance where userid = %s'''
        my_cursor.execute(sql, userid)
        select_data = my_cursor.fetchone()
        connection.commit()
        connection.close()
        res = select_data['wallet_balance']
        return res
    except Exception as e:
        print(e)
        print('bitmex_mysqldb.balance_select error')
        return 0



def revenue_update(data, userid):
    try:
        connection = sqlsetting.mysqlset()
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''INSERT INTO trade.revenue (revenue, userid) VALUES (%s, %s) ON DUPLICATE KEY UPDATE revenue=%s'''
        my_cursor.execute(sql, (str(data), userid, str(data)))
        connection.commit()
        connection.close()
    except Exception as e:
        print(e)
        print('bitmex_mysqldb.revenue_update error')


def revenue_select(userid):
    try:
        connection = sqlsetting.mysqlset()
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''select revenue from trade.revenue where userid = %s'''
        my_cursor.execute(sql, userid)
        select_data = my_cursor.fetchone()
        connection.commit()
        connection.close()
        if select_data is None:
            pass
            return [0,0,0,0]
        else:
            res = eval(select_data['revenue'])
            return res
    except Exception as e:
        print(e)
        print('bitmex_mysqldb.revenue_update error')
        return [0, 0, 0, 0]



def orderlist_update(data, userid):
    try:
        connection = sqlsetting.mysqlset()
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''INSERT INTO trade.get_order_list (get_order, userid) VALUES (%s, %s) ON DUPLICATE KEY UPDATE get_order=%s'''
        my_cursor.execute(sql, (str(data), userid, str(data)))
        connection.commit()
        connection.close()
    except Exception as e:
        print(e)
        print('bitmex_mysqldb.orderlist_update error')


def orderlist_select(userid):
    try:
        connection = sqlsetting.mysqlset()
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''select get_order from trade.get_order_list where userid = %s'''
        my_cursor.execute(sql, userid)
        select_data = my_cursor.fetchone()
        connection.commit()
        connection.close()
        res = eval(select_data['get_order'])
        return res
    except Exception as e:
        print(e)
        print('bitmex_mysqldb.orderlist_update error')


def settingValue(userid):
    try:
        ''' 셋팅값 가져오기 '''
        connection = sqlsetting.mysqlset()
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''select * from trade.bitmex_setting where userid = %s'''
        my_cursor.execute(sql, userid)
        select_data = my_cursor.fetchone()
        connection.commit()
        connection.close()
        return select_data
    except Exception as e:
        print(e)
        print('bitmex_mysqldb.settingValue error')


def insert_ordid(orderdata, userid):
    try:
        '''주문내역 저장'''
        connection = sqlsetting.mysqlset()
        time = datetime.datetime.strptime(str(orderdata['transactTime']),'%Y-%m-%dT%H:%M:%S.%fZ')+ datetime.timedelta(hours=9)
        market = orderdata['symbol']
        ordId = orderdata['orderID']
        user_id = userid
        state = '1'
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''insert into trade.bitmex_ordidlist(time, market, ordId, userid, state) 
                SELECT %s, %s, %s, %s, %s FROM dual where not exists(select ordId from trade.bitmex_ordidlist where ordId = %s and userid = %s)'''
        my_cursor.execute(sql, (time, market, ordId, user_id, state, ordId, user_id))
        connection.commit()
        connection.close()
    except Exception as e:
        print(e)
        print('bitmex_mysqldb.insert_ordid error')
    
    
def select_ordid(marketid, userid):
    try:
        ''' 주문내역 가져오기 '''
        connection = sqlsetting.mysqlset()
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''select * from trade.bitmex_ordidlist where market = %s and userid = %s and state = %s '''
        my_cursor.execute(sql, (marketid, userid, str(1)))
        select_data = my_cursor.fetchall()
        connection.commit()
        connection.close()
        return select_data
    except Exception as e:
        print(e)
        print('bitmex_mysqldb.select_ordid error')


def update_ordid(data, status):
    try:
        ''' 주문내역 업데이트 '''
        connection = sqlsetting.mysqlset()
        for i in data:
            state = status
            ordId = i['orderID']
            my_cursor = connection.cursor(pymysql.cursors.DictCursor)
            sql = '''update trade.bitmex_ordidlist set state = %s where ordId = %s'''
            my_cursor.execute(sql, (state, ordId))
            connection.commit()
        connection.close()
        return
    except Exception as e:
        print(e)
        print('mysqlddb.update_ordid error')


def insert_data(getorder, user_id):
    try:
        ''' 거래내역 저장 '''
        connection = sqlsetting.mysqlset()
        if len(getorder) > 0:
            for i in getorder:
                order_time = datetime.datetime.strptime(str(i['transactTime']),'%Y-%m-%dT%H:%M:%S.%fZ')+ datetime.timedelta(hours=9)
                transact_time = datetime.datetime.strptime(str(i['timestamp']),'%Y-%m-%dT%H:%M:%S.%fZ')+ datetime.timedelta(hours=9)
                market = i['symbol']
                ordId = i['orderID']
                side = i['side']
                price = i['price']
                unit = i['cumQty']
                ordertype = i['ordType']
                if i['ordType'] == 'Market':
                    fee = -int(((unit/price)*0.0005)*100000000)/100000000
                else:
                    fee = int(((unit/price)*0.0001)*100000000)/100000000
                orderstate = i['ordStatus']
                my_cursor = connection.cursor(pymysql.cursors.DictCursor)
                sql = '''insert into trade.bitmex_orderhistory(order_time, market, side, price, unit, fee, ordertype, transact_time, userid, ordId, orderstate, last_order) 
                SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 0 FROM dual where not exists(select ordId from trade.bitmex_orderhistory where ordId = %s and userid = %s)'''
                my_cursor.execute(sql,(order_time, market, side, price, unit, fee, ordertype, transact_time, user_id, ordId, orderstate, ordId, user_id))
                connection.commit()
            connection.close()
            return
    except Exception as e:
        print(e)
        print('bitmex_insert_data : error')


def onoff_Status(user_id):
    try:
        connection = sqlsetting.mysqlset()
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''select * from trade.bitmex_setting where userid = %s'''
        my_cursor.execute(sql, user_id)
        select_data = my_cursor.fetchone()
        connection.commit()
        connection.close()
        if select_data['stoploss_onoff'] == 0:
            stoploss_onoff = 'off'
        else:
            stoploss_onoff = 'on'

        if select_data['botstatus'] == 0:
            botstatus = 'off'
        else:
            botstatus = 'on'

        if select_data['appointment'] == 0:
            appointment = 'off'
        else:
            appointment = 'on'

        return {'botstatus' : botstatus, 'stoploss_onoff' : stoploss_onoff, 'appointment' : appointment}
    except Exception as e:
        print(e)
        print('bitmex stoplossStatus error')


def botUpdate(user_id):
    try:
        connection = sqlsetting.mysqlset()
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''select * from trade.bitmex_setting where userid = %s'''
        my_cursor.execute(sql, user_id)
        select_data = my_cursor.fetchone()

        if select_data['botstatus'] == 0:
            my_cursor = connection.cursor(pymysql.cursors.DictCursor)
            sql = '''update trade.bitmex_setting set botstatus = 1 where userid = %s'''
            my_cursor.execute(sql, user_id)
            connection.commit()
            connection.close()

        else:
            my_cursor = connection.cursor(pymysql.cursors.DictCursor)
            sql = '''update trade.bitmex_setting set botstatus = 0 where userid = %s'''
            my_cursor.execute(sql, user_id)
            connection.commit()
            connection.close()
    except Exception as e:
        print(e)
        print('bitmex botUpdate error')


def bitmex_stoploss(user_id):
    try:
        print('bitmex_stoploss')
        connection = sqlsetting.mysqlset()
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''select * from trade.bitmex_setting where userid = %s'''
        my_cursor.execute(sql, user_id)
        select_data = my_cursor.fetchone()

        if select_data['stoploss_onoff'] == 0:
            my_cursor = connection.cursor(pymysql.cursors.DictCursor)
            sql = '''update trade.bitmex_setting set stoploss_onoff = 1 where userid = %s'''
            my_cursor.execute(sql, user_id)
            connection.commit()
            connection.close()

        else:
            my_cursor = connection.cursor(pymysql.cursors.DictCursor)
            sql = '''update trade.bitmex_setting set stoploss_onoff = 0 where userid = %s'''
            my_cursor.execute(sql, user_id)
            connection.commit()
            connection.close()
    except Exception as e:
        print(e)
        print('bitmex stoploss_onoff error')


def bitmex_appointment(user_id):
    try:
        print('bitmex_appointment')
        connection = sqlsetting.mysqlset()
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''select * from trade.bitmex_setting where userid = %s'''
        my_cursor.execute(sql, user_id)
        select_data = my_cursor.fetchone()

        if select_data['appointment'] == 0:
            my_cursor = connection.cursor(pymysql.cursors.DictCursor)
            sql = '''update trade.bitmex_setting set appointment = 1 where userid = %s'''
            my_cursor.execute(sql, user_id)
            connection.commit()
            connection.close()

        else:
            my_cursor = connection.cursor(pymysql.cursors.DictCursor)
            sql = '''update trade.bitmex_setting set appointment = 0 where userid = %s'''
            my_cursor.execute(sql, user_id)
            connection.commit()
            connection.close()
    except Exception as e:
        print(e)
        print('bitmex stoploss_onoff error')



def lastorder_update(price, market, user_id, entry_position):
    try:
        if entry_position == 'long':
            connection = sqlsetting.mysqlset()
            my_cursor = connection.cursor(pymysql.cursors.DictCursor)
            sql = '''update trade.bitmex_orderhistory set last_order = %s where market = %s and side = 'Buy' and ordertype = 'Market' and  userid = %s order by transact_time DESC limit 1'''
            my_cursor.execute(sql, (float(price), market, user_id))
            connection.commit()
            connection.close()
        else:
            connection = sqlsetting.mysqlset()
            my_cursor = connection.cursor(pymysql.cursors.DictCursor)
            sql = '''update trade.bitmex_orderhistory set last_order = %s where market = %s and side = 'Sell' and  ordertype = 'Market' and  userid = %s order by transact_time DESC limit 1'''
            my_cursor.execute(sql, (float(price), market, user_id))
            connection.commit()
            connection.close()
        return
    except Exception as e:
        print(e)
        print('bitmex lastorder_update error')


def lastorder_select(market, user_id, entry_position):
    try:
        if entry_position == 'long':
            connection = sqlsetting.mysqlset()
            my_cursor = connection.cursor(pymysql.cursors.DictCursor)
            sql = '''select * from trade.bitmex_orderhistory where side = 'Buy' and market = %s and ordertype = 'Market' and userid = %s order by transact_time DESC limit 1'''
            my_cursor.execute(sql, (market, user_id))
            select_data = my_cursor.fetchone()
            connection.commit()
            connection.close()
        else:
            connection = sqlsetting.mysqlset()
            my_cursor = connection.cursor(pymysql.cursors.DictCursor)
            sql = '''select * from trade.bitmex_orderhistory where side = 'Sell' and market = %s and ordertype = 'Market' and userid = %s order by transact_time DESC limit 1'''
            my_cursor.execute(sql, (market, user_id))
            select_data = my_cursor.fetchone()
            connection.commit()
            connection.close()
        return select_data['last_order']
    except Exception as e:
        print(e)
        print('bitmex lastorder_select error')


def buyintervalStatus(user_id):
    try:
        connection = sqlsetting.mysqlset()
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''select * from trade.bitmex_buyintervalset where userid = %s'''
        my_cursor.execute(sql, user_id)
        select_data = my_cursor.fetchone()
        data = [select_data['buy_1'], select_data['buy_2'], select_data['buy_3'], select_data['buy_4'], select_data['buy_5'], select_data['buy_6'], select_data['buy_7'], select_data['buy_8'], select_data['buy_9']]
        connection.commit()
        connection.close()
        return data
    except Exception as e:
        print(e)
        print('bitmex buyintervalstatus error')


def buyintervalset(data, user_id):
    try:
        connection = sqlsetting.mysqlset()
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''update trade.bitmex_buyintervalset set buy_1 = %s, buy_2 = %s, buy_3 = %s, buy_4 = %s, buy_5 = %s, buy_6 = %s, buy_7 = %s, buy_8= %s, buy_9 = %s where userid = %s'''
        my_cursor.execute(sql, (
        float(data[0]),float(data[1]),float(data[2]),float(data[3]),float(data[4]),float(data[5]),float(data[6]),float(data[7]),float(data[8]), user_id))
        connection.commit()
        connection.close()
    except Exception as e:
        print(e)
        print('bitmex buyintervalstatus error')



def botUpdate2(user_id):
    try:
        connection = sqlsetting.mysqlset()
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''update trade.bitmex_setting set botstatus = 0, appointment = 0 where userid = %s'''
        my_cursor.execute(sql, user_id)
        connection.commit()
        connection.close()
    except Exception as e:
        print(e)
        print('bitmex botUpdate2 error')




def firstbuy_select(market, user_id, entry_position):
    try:
        if entry_position == 'long':
            connection = sqlsetting.mysqlset()
            my_cursor = connection.cursor(pymysql.cursors.DictCursor)
            sql = '''select * from trade.bitmex_orderhistory where market = %s and side = 'Buy' and ordertype = 'Market' and userid = %s order by  transact_time DESC limit 1 '''
            my_cursor.execute(sql, (market, user_id))
            select_data = my_cursor.fetchone()
            connection.commit()
            connection.close()
        else:
            connection = sqlsetting.mysqlset()
            my_cursor = connection.cursor(pymysql.cursors.DictCursor)
            sql = '''select * from trade.bitmex_orderhistory where market = %s and side = 'Sell' and ordertype = 'Market' and userid = %s order by  transact_time DESC limit 1 '''
            my_cursor.execute(sql, (market, user_id))
            select_data = my_cursor.fetchone()
            connection.commit()
            connection.close()
        return select_data['price']
    except Exception as e:
        print(e)
        print('bitmex firstbuy_select error')


def setting_update(data, user_id):
    try:
        connection = sqlsetting.mysqlset()
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''update trade.bitmex_setting set currency = %s, start_payment = %s, count = %s, positionsell = %s, loss_stop = %s , entry_position = %swhere userid = %s'''
        my_cursor.execute(sql, (str(data[4]), float(data[0]), int(data[1]), float(data[2]), float(data[3]), str(data[5]), user_id))
        connection.commit()
        connection.close()
    except Exception as e:
        print(e)
        print('bitmex firstbuy_select error')



def select_orddata(data, user_id):
    try:
        connection = sqlsetting.mysqlset()
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''select * from trade.bitmex_orderhistory where market = %s and userid= %s'''
        my_cursor.execute(sql, (data, user_id))
        select_data = my_cursor.fetchall()
        connection.commit()
        connection.close()
        select_data = sorted(select_data, key=lambda person: (person['transact_time']), reverse=True)
        # print(select_data)
        buy_price = 0
        buy_valume = 0
        buy_fee = 0
        sell_price = 0
        sell_valume = 0
        sell_fee = 0

        count = 0
        count2 = 0
        if len(select_data) > 0:
            for i in select_data:
                if i['side'] == 'Buy':
                    buy_price += float(i['unit'])/float(i['price'])  # 체결가격
                    buy_valume += float(i['unit'])  # 체결수량
                    buy_fee += float(i['fee']) # 수수료
                    count2 += 1
                else:
                    sell_price += float(i['unit'])/float(i['price'])  # 체결가격
                    sell_valume += float(i['unit'])  # 체결수량
                    sell_fee += float(i['fee'])  # 수수료

            # if buy_valume != 0 and sell_valume != 0:
            trade_vol = sell_price + buy_price # 거래량
            trade_vol2 = buy_price - sell_price
            rate = trade_vol2 + sell_fee + buy_fee # 수익
            return rate, trade_vol
        else:
            return 0, 0
    except Exception as e:
        print(e)
        print('bitmex_select_orddata error')
        return 0, 0


def get_ticker(market):
    try:
        connection = sqlsetting.mysqlset()
        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''select * from trade.bitmex_price where market = %s'''
        my_cursor.execute(sql, market)
        select_data = my_cursor.fetchone()
        connection.commit()
        connection.close()
        return select_data['price']
    except Exception as e:
        print(e)
        print('bitmex get_ticker error')