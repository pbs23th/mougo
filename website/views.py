from flask import Blueprint, render_template, request, flash, redirect, jsonify, session
from flask_login import login_required, current_user
import pymysql
import pyupbit
import datetime
from . import okex_mysqldb
from . import okex_Api
from . import upbit_mysqldb
from . import upbit_Api
from . import bitmexAPI
from . import sqlsetting
import db_query.user as user
import okex.Market_api as Market
import okex.Account_api as Account
import okex.Trade_api as Trade

views = Blueprint('views', __name__)


''' OKEX ROUTE '''
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    print('test')
    data = {}
    return render_template("home.html", user=current_user, data=data)



@views.route('/apisetting', methods=['GET'])
def apisetting():
    user_id = session['_user_id']
    userstatus = user.user(user_id)
    username =  userstatus['username']
    api_key = user.api_key(user_id)
    print(api_key)
    return render_template("apiSetting.html", user=current_user, api_key=api_key, username=username)


@views.route('/apisetting', methods=['POST'])
def insert_apisetting():
    try:
        user_id = session['_user_id']
        accessKey = request.form['accessKey']
        secretKey = request.form['secretKey']
        passphrase = request.form['passphrase']
        exchange = request.form['exchange']
        if exchange == 'UPBIT':
            upbit = pyupbit.Upbit(accessKey, secretKey)
            res = upbit.get_balances()
            if str(type(res)) == "<class 'dict'>" :
                if res.get('error'):
                    print('error')
                    return False
            else:
                insert_api = user.insert_api_key(user_id, exchange, accessKey, secretKey, passphrase)
                if insert_api == 'seccess':
                    res = user.select_api_key(user_id)
                    bot_id = res[0]
                    res2 = user.insert_user_data(bot_id)

        elif exchange == 'OKEX':
            okex = Account.AccountAPI(accessKey, secretKey, passphrase, False)
            res = okex.get_account()
            if res['code'] == '0':
                insert_api = user.insert_api_key(user_id, exchange, accessKey, secretKey, passphrase)

        elif exchange == 'BITMEX':
            bitmex = bitmexAPI.Bitmex(accessKey, secretKey)
            res = bitmex.bitmex_my_balance()
            if res['currency']:
                insert_api = user.insert_api_key(user_id, exchange, accessKey, secretKey, passphrase)
        else:
            pass

        return 'success'

    except Exception as e:
        return False


@views.route('/apisetting', methods=['DELETE'])
def delete_apisetting():
    print('delete')
    number = request.form['index']
    user.update_api_key(number)
    return 'success'














































@views.route('/okex_bot', methods=['GET', 'POST'])
@login_required
def okex_botonoff():
    try:
        user_id = current_user.id
        okex_settingValue = okex_mysqldb.settingValue(user_id)
        okexuser = okex_mysqldb.userValue(user_id)
        username = okexuser['username']
        data = okex_mysqldb.botStatus(user_id)
        buydata = okex_mysqldb.buyintervalStatus(user_id)
        api_key = okex_settingValue['apikey']
        secret_key = okex_settingValue['secretkey']
        passphrase = okex_settingValue['passphrase']
        currency = okex_settingValue['currency']
        payment = okex_settingValue['payment']
        stepprice = str(okex_settingValue['stepprice'])
        unitformat = str(okex_settingValue['unitformat'])
        flag = '0'  # 实盘 real trading
        stoploss_onoff = okex_mysqldb.stoplossStatus(user_id)
        appointment = okex_mysqldb.appointmentStatus(user_id)
        accountAPI = Account.AccountAPI(api_key, secret_key, passphrase, False, flag)
        tradeAPI = Trade.TradeAPI(api_key, secret_key, passphrase, False, flag)
        accountAPIdata = accountAPI.get_account(payment)
        accountAPIdata2 = accountAPI.get_account(currency)
        if len(accountAPIdata['data'][0]['details']) > 0:
            payment_bal = accountAPIdata['data'][0]['details'][0]['cashBal']
        else:
            payment_bal = 0
        if len(accountAPIdata2['data'][0]['details']) > 0:
            currency_bal = accountAPIdata2['data'][0]['details'][0]['cashBal']
        else:
            currency_bal = 0

        if payment_bal == None:
            okex_settingValue = {
                'apikey' : ' apikey 확인요망',
                'secretkey' : ' secretkey 확인요망',
                'currency' : ' ',
                'start_payment' : 0,
            }
            payment_bal = 0
            getorders = None
            print('payment_bal = None')
            return redirect('apisetting')
        else:
            getorder = tradeAPI.get_order_list(instType='SPOT', instId=currency+'-'+payment)
            getorder = getorder['data']
            getorders = sorted(getorder, key=lambda person: (float(person['px'])),reverse=True)
            if len(getorder) > 0:
                sum = 0
                for i in getorders:
                    i['sz'] = float(i['sz'])
                    sum += float(i['px']) * float(i['sz'])
                    i['sum'] = sum
                    i['usdt'] = float(i['px']) * float(i['sz'])
                    i['cTime'] = datetime.datetime.utcfromtimestamp(int(i['cTime'][:10]))+datetime.timedelta(hours=9)


        if data == 400:
            flash('세팅값이 없습니다 !', category='error')
            return redirect('apisetting')
        #
        if request.method == 'POST':
            okex_mysqldb.botUpdate(user_id)
            data = okex_mysqldb.botStatus(user_id)
            okex_settingValue = okex_mysqldb.settingValue(user_id)
            t1 = okex_Api.Worker('okex'+str(user_id))
            t1.run()
            print('t1 start'+str(user_id))
            return data

        revenue2 = okex_Api.Api().avg_price()
        vol = revenue2[1]
        revenue = revenue2[0]
        return render_template("okex_bot.html", user=current_user, stoploss_onoff=stoploss_onoff, data=data, data2=buydata, settingValue=okex_settingValue,
                               payment_bal=float(payment_bal), currency_bal=float(currency_bal), tables=getorders, appointment=appointment, username=username, revenue=revenue, vol=int(vol))
    except Exception as e:
        print(e)
        return redirect('apisetting')



@views.route('/okex_get_revenue')
def okex_get_revenue():
    revenue2 = okex_Api.Api().avg_price()
    ticker = okex_Api.Api().get_price()
    vol = int(revenue2[1])
    revenue = revenue2[0]
    avgprice = revenue2[2]
    return jsonify([revenue,vol, avgprice, ticker])



@views.route('/okex_get_order_list')
def okex_get_order_list():
    user_id = current_user.id
    okex_settingValue = okex_mysqldb.settingValue(user_id)
    api_key = okex_settingValue['apikey']
    secret_key = okex_settingValue['secretkey']
    passphrase = okex_settingValue['passphrase']
    flag = '0'  # 实盘 real trading
    tradeAPI = Trade.TradeAPI(api_key, secret_key, passphrase, False, flag)
    currency = okex_settingValue['currency']
    payment = okex_settingValue['payment']
    getorder = tradeAPI.get_order_list(instType='SPOT', instId=currency + '-' + payment)
    getorder = getorder['data']
    getorders = sorted(getorder, key=lambda person: (float(person['px'])), reverse=True)
    if len(getorder) > 0:
        sum = 0
        for i in getorders:
            sum += float(i['px']) * float(i['sz'])
            i['sum'] = sum
            i['usdt'] = float(i['px']) * float(i['sz'])
            i['cTime'] = datetime.datetime.utcfromtimestamp(int(i['cTime'][:10])) + datetime.timedelta(hours=9)
    return jsonify(getorder=getorders)


@views.route('/okex_cancelall', methods=['POST'])
@login_required
def okex_cancelall():
    print('okex_cancelall')
    if request.method == 'POST':
        okex_Api.Api().cancelsell()
        okex_Api.Api().cancelbuy()
        # okex_Api.Api().select_ordidlist()
        return 'ok'
    return 'ok'


@views.route('/okex_sellall', methods=['POST'])
@login_required
def okex_sellall():
    if request.method == 'POST':
        okex_Api.Api().sellposition()
        # okex_Api.Api().select_ordidlist()
        return 'ok'
    return 'ok'


@views.route('/okex_buyupdate', methods=['POST'])
def okex_buyupdate():
    if request.method == 'POST':
        okex_Api.Api().buylist()
        return 'ok'
    return 'ok'


@views.route('/okex_stoploss', methods=['GET', 'POST'])
def okex_stoploss():
    
    print('okex_stoploss')
    if request.method == 'POST':
        user_id = current_user.id
        okex_mysqldb.stoplossUpdate(user_id)
        return 'ok'
    return 'ok'


@views.route('/okex_appointment', methods=['GET', 'POST'])
def okex_appointmentUpdate():
    user_id = current_user.id
    if request.method == 'POST':
        okex_mysqldb.appointmentUpdate(user_id)
        return 'ok'
    return 'ok'


@views.route('/okex_buyintervalset', methods=['GET', 'POST'])
def okex_buyintervalset():
    user_id = current_user.id
    connection = sqlsetting.mysqlset()
    if request.method == 'POST':
        buy_1 = request.form['buy1']
        buy_2 = request.form['buy2']
        buy_3 = request.form['buy3']
        buy_4 = request.form['buy4']
        buy_5 = request.form['buy5']
        buy_6 = request.form['buy6']
        buy_7 = request.form['buy7']
        buy_8 = request.form['buy8']
        buy_9 = request.form['buy9']

        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''select * from trade.okex_buyintervalset where userid = %s'''
        my_cursor.execute(sql, user_id)
        select_data = my_cursor.fetchone()
        connection.commit()

        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''update trade.okex_buyintervalset set buy_1 = %s, buy_2 = %s, buy_3 = %s, buy_4 = %s, buy_5 = %s, buy_6 = %s, buy_7 = %s, buy_8= %s, buy_9 = %s where userid = %s'''
        my_cursor.execute(sql, (float(buy_1), float(buy_2), float(buy_3), float(buy_4), float(buy_5), float(buy_6), float(buy_7), float(buy_8), float(buy_9), user_id))
        connection.commit()
        connection.close()
        return 'ok'


    my_cursor = connection.cursor(pymysql.cursors.DictCursor)
    sql = '''select * from trade.okex_buyintervalset where userid = %s'''
    my_cursor.execute(sql, user_id)
    select_data = my_cursor.fetchone()
    connection.commit()
    connection.close()

    return 'ok'



@views.route('/okex_settings', methods=['POST'])
def okex_settings():
    user_id = current_user.id
    connection = sqlsetting.mysqlset()
    if request.method == 'POST':
        print('okex_settings')
        start_payment = request.form['start_payment']
        count = request.form['count']
        positionsell = request.form['positionsell']
        loss_stop = request.form['loss_stop']
        currency = request.form['currency'].upper()
        payment = request.form['payment'].upper()

        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''select * from trade.okex_setting where userid = %s'''
        my_cursor.execute(sql, user_id)
        select_data = my_cursor.fetchone()
        connection.commit()

        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''update trade.okex_setting set currency = %s, start_payment = %s, count = %s, positionsell = %s, loss_stop = %s , payment = %s where userid = %s'''
        my_cursor.execute(sql, (str(currency), float(start_payment), int(count), float(positionsell), float(loss_stop), str(payment), user_id))
        connection.commit()
        connection.close()
        return 'ok'

    my_cursor = connection.cursor(pymysql.cursors.DictCursor)
    sql = '''select * from trade.okex_setting where userid = %s'''
    my_cursor.execute(sql, user_id)
    select_data = my_cursor.fetchone()
    connection.commit()
    connection.close()
    return 'ok'





@views.route('/okex_get_ticker')
@login_required
def okex_get_ticker():
    ticker = okex_Api.Api().get_price()
    return jsonify(ticker=ticker)




# ''' UPBIT ROUTE'''
@views.route('/upbit_bot/test', methods=['GET', 'POST'])
@login_required
def upbit_botonoff():
    try:
        user_id = session['_user_id']
        print(user_id)
        settingValue = upbit_mysqldb.settingValue(user_id)
        data = upbit_mysqldb.botStatus(user_id)
        okexuser = user.user(user_id)
        bot = user.select_api_key(user_id)
        username = okexuser['username']
        access_key = bot[0]['access_key']
        secret_key = bot[0]['secret_key']
        bot_id = 21
        settingValue = user.select_bot_setting(bot_id)
        print('-----------------------------')
        print(settingValue)
        print('-----------------------------')
        currency = settingValue['currency']
        appointment = 'off'
        buydata = user.buyintervalStatus(bot_id)
        stoploss_onoff = upbit_mysqldb.stoplossStatus(user_id)
        upbit = pyupbit.Upbit(access_key, secret_key)
        currency_bal = upbit.get_balance_t(currency)
        payment_bal = upbit.get_balance_t()
        # if currency_bal == None:
        #     settingValue = {
        #         'apikey': ' apikey 확인요망',
        #         'secretkey': ' secretkey 확인요망',
        #         'currency': ' ',
        #         'start_payment': 0,
        #     }
        #     currency_bal = 0
        #     getorders = None
        #     print('volume = None')
        #     return redirect('apisetting')
        # else:
        #     getorder = upbit.get_order('KRW-' + currency, state='wait')
        #     getorders = sorted(getorder, key=lambda person: (person['price']), reverse=True)
        #     if len(getorders) > 0:
        #         sum = 0
        #         for i in getorders:
        #             sum += int(float(i['price']) * float(i['volume']))
        #             i['sum'] = sum
        #             i['krw'] = int(float(i['price']) * float(i['volume']))
        #             i['created_at'] = i['created_at'][:-6]

        # if request.method == 'POST':
        #     upbit_mysqldb.botUpdate(user_id)
        #     data = upbit_mysqldb.botStatus(user_id)
        #     settingValue = upbit_mysqldb.settingValue(user_id)
        #     # if data == 'on':
        #     t2 = upbit_Api.Worker('upbit'+str(user_id))
        #     t2.run()
        #     print('t2 start')
        return jsonify(settingValue)
            #render_template("upbit_bot.html", user=current_user, payment_bal=int(payment_bal), stoploss_onoff=stoploss_onoff, data=data, currency_bal=float(currency_bal), settingValue=settingValue, tables=getorders, data2=buydata, username=username, appointment=appointment)

    except Exception as e:
        print(e)
        return e


@views.route('/upbit_get_order_list', methods=['GET', 'POST'])
@login_required
def upbit_get_order_list():
    user_id = current_user.id
    upbit_settingValue = upbit_mysqldb.settingValue(user_id)
    api_key = upbit_settingValue['apikey']
    secret_key = upbit_settingValue['secretkey']
    currency = upbit_settingValue['currency']
    payment = upbit_settingValue['payment']
    upbit = pyupbit.Upbit(api_key, secret_key)
    getorder = upbit.get_order('KRW-' + currency, state='wait')
    getorders = sorted(getorder, key=lambda person: (person['price']), reverse=True)
    if len(getorder) > 0:
        sum = 0
        for i in getorders:
            sum += int(float(i['price']) * float(i['volume']))
            i['sum'] = sum
            i['krw'] = int(float(i['price']) * float(i['volume']))
            i['created_at'] = i['created_at'][:-6]
    return jsonify(getorder=getorders)





@views.route('/upbit_settings', methods=['POST'])
def upbit_settings():
    user_id = current_user.id
    connection = pymysql.connect(
        user='gmc',
        port=3306,
        passwd='Gmc1234!',
        host='127.0.0.1',
        db='trade',
        charset='utf8'
    )
    if request.method == 'POST':
        print('upbit_settings')
        start_payment = request.form['start_payment']
        count = request.form['count']
        positionsell = request.form['positionsell']
        loss_stop = request.form['loss_stop']
        currency = request.form['currency'].upper()

        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''select * from trade.upbit_setting where userid = %s'''
        my_cursor.execute(sql, user_id)
        select_data = my_cursor.fetchone()
        connection.commit()

        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''update trade.upbit_setting set currency = %s, start_payment = %s, count = %s, positionsell = %s, loss_stop = %s where userid = %s'''
        my_cursor.execute(sql, (str(currency), float(start_payment), int(count), float(positionsell), float(loss_stop), user_id))
        connection.commit()
        connection.close()
        return "ok"

    my_cursor = connection.cursor(pymysql.cursors.DictCursor)
    sql = '''select * from trade.upbit_setting where userid = %s'''
    my_cursor.execute(sql, user_id)
    select_data = my_cursor.fetchone()
    connection.commit()
    connection.close()
    return "ok"


@views.route('/upbit_buyintervalset', methods=['GET', 'POST'])
def upbit_buyintervalset():
    user_id = current_user.id
    print('upbit_buyintervalset')
    connection = pymysql.connect(
        user='gmc',
        port=3306,
        passwd='Gmc1234!',
        host='127.0.0.1',
        db='trade',
        charset='utf8'
    )
    if request.method == 'POST':
        buy_1 = request.form['buy1']
        buy_2 = request.form['buy2']
        buy_3 = request.form['buy3']
        buy_4 = request.form['buy4']
        buy_5 = request.form['buy5']
        buy_6 = request.form['buy6']
        buy_7 = request.form['buy7']
        buy_8 = request.form['buy8']
        buy_9 = request.form['buy9']

        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''select * from trade.upbit_buyintervalset where userid = %s'''
        my_cursor.execute(sql, user_id)
        select_data = my_cursor.fetchone()
        connection.commit()

        my_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = '''update trade.upbit_buyintervalset set buy_1 = %s, buy_2 = %s, buy_3 = %s, buy_4 = %s, buy_5 = %s, buy_6 = %s, buy_7 = %s, buy_8= %s, buy_9 = %s where userid = %s'''
        my_cursor.execute(sql, (float(buy_1), float(buy_2), float(buy_3), float(buy_4), float(buy_5), float(buy_6), float(buy_7), float(buy_8), float(buy_9), user_id))
        connection.commit()
        connection.close()
        return 'ok'

    my_cursor = connection.cursor(pymysql.cursors.DictCursor)
    sql = '''select * from trade.upbit_buyintervalset where userid = %s'''
    my_cursor.execute(sql, user_id)
    select_data = my_cursor.fetchone()
    connection.commit()
    connection.close()
    return 'ok'



@views.route('/upbit_cancelall', methods=['POST'])
@login_required
def upbit_cancelall():
    print('upbit_cancelall')
    if request.method == 'POST':
        upbit_Api.Api().cancelsell()
        upbit_Api.Api().cancelbuy()

        return "ok"
    return "ok"


@views.route('/upbit_sellall', methods=['POST'])
@login_required
def upbit_sellall():
    if request.method == 'POST':
        upbit_Api.Api().sellposition()
        return "ok"
    return "ok"


@views.route('/upbit_buyupdate', methods=['POST'])
@login_required
def upbit_buyupdate():
    if request.method == 'POST':
        upbit_Api.Api().buylist()
        return "ok"
    return "ok"


@views.route('/upbit_stoploss', methods=['POST'])
def upbit_stoploss():
    user_id = current_user.id
    print('upbit_stoploss')
    if request.method == 'POST':
        upbit_mysqldb.stoplossUpdate(user_id)
        return "ok"
    return "ok"



@views.route('/upbit_appointment', methods=['POST'])
def upbit_appointmentUpdate():
    user_id = current_user.id
    print('upbit_appointment')
    if request.method == 'POST':
        upbit_mysqldb.appointmentUpdate(user_id)
        return "ok"
    return "ok"



@views.route('/upbit_apisetting', methods=['POST'])
def upbit_apisetting():
    user_id = current_user.id
    print('upbit_apisetting')
    userstatus = okex_mysqldb.userValue(user_id)
    username =  userstatus['username']
    if request.method == "POST":
        connection = sqlsetting.mysqlset()
        apikey = request.form['accessKey']
        secretKey = request.form['secretKey']
        upbit = pyupbit.Upbit(apikey,secretKey)
        data = upbit.get_balances()

        if str(type(data)) == "<class 'dict'>" :
            if data.get('error'):
                print('error')
                return False
        else:
            print('apikey update')
            my_cursor = connection.cursor(pymysql.cursors.DictCursor)
            sql = '''update trade.upbit_setting set apikey = %s, secretkey = %s where userid = %s'''
            my_cursor.execute(sql, (str(apikey), str(secretKey), user_id))
            connection.commit()

        connection.close()
        return 'POST'

    return 'GET'


@views.route('/upbit_get_ticker')
def upbit_get_ticker():
    ticker = upbit_Api.Api().get_price()
    return jsonify(ticker=ticker)


@views.route('/min_sz')
def min_sz():
    min_sz = okex_mysqldb.min_sz("DOGE-USDT")
    return jsonify(min_sz=min_sz)


@views.route('/upbit_get_revenue')
def upbit_get_revenue():
    revenue2 = upbit_Api.Api().revenue()
    ticker = upbit_Api.Api().get_price()
    vol = int(revenue2[1])
    revenue = int(revenue2[0])
    avgprice = upbit_Api.Api().avg_price()
    return jsonify([revenue,vol, avgprice, ticker])