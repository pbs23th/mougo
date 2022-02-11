from flask import Blueprint ,render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_user, login_required, logout_user, current_user
import pymysql
from . import bitmex_mysqldb
from . import bitmex_Api
from . import sqlsetting
from . import bitmexAPI

bitmex = Blueprint('bitmex', __name__)

@bitmex.route("/bitmex_bot", methods=['GET', 'POST'])
def bitmex_bot():
    # try:
    user_id = current_user.id
    bitmex_settingValue = bitmex_mysqldb.settingValue(user_id)
    get_price = bitmex_Api.Api().get_price()
    avg_data = bitmex_Api.Api().avg_price()
    payment_bal = bitmex_Api.Api().get_balance()
    onoff_Status = bitmex_mysqldb.onoff_Status(user_id)
    buydata = bitmex_mysqldb.buyintervalStatus(user_id)
    data = onoff_Status['botstatus']
    stoploss_onoff = onoff_Status['stoploss_onoff']
    appointment = onoff_Status['appointment']
    bitmex_Api.Api().select_revenue()
    if avg_data is None:
        avg_price = 0
        currency_bal = 0
    elif avg_data[0] is None:
        avg_price = 0
        currency_bal = 0
    else:
        avg_price = avg_data[0]
        currency_bal = avg_data[1]

    if avg_price == 0:
        rate = 0
    else:
        rate = int(((get_price - avg_price)/avg_price)*10000)/100

    # getorders = bitmex_Api.Api().get_open_order()

    #
    if request.method == 'POST':
        bitmex_mysqldb.botUpdate(user_id)
        # data = okex_mysqldb.botStatus(user_id)
        # bitmex_settingValue = bitmex_mysqldb.settingValue(user_id)
        t1 = bitmex_Api.Worker('bitmex'+str(user_id))
        t1.run()
        print('t1 start'+str(user_id))
        return data

    # revenue2 = okex_Api.Api().avg_price()
    vol = 0
    revenue = 0
    wallet = bitmex_Api.Api().wallet_balance()

    return render_template("bitmex_bot.html", user=current_user, stoploss_onoff=stoploss_onoff, data=data, data2=buydata, settingValue=bitmex_settingValue,
                           payment_bal=payment_bal, currency_bal=currency_bal, tables=[], appointment=appointment, revenue=revenue, vol=int(vol), ticker=get_price, avg_price=avg_price, rate=rate, wallet=wallet)
    # except Exception as e:
    #     print(e)
    #     return redirect('apisetting')


@bitmex.route("/get_ticker", methods=['GET'])
def get_ticker():
    try:
        user_id = current_user.id
        get_price = bitmex_mysqldb.get_price(user_id)
        # print(res)
        return jsonify(get_price)
    except:
        pass


@bitmex.route("/avg_price", methods=['GET'])
def avg_price():
    try:
        avg_data = bitmex_Api.Api().avg_price()
        avg_price = avg_data[0]
        avg_unit = avg_data[1]
        return jsonify([avg_price,avg_unit])
    except:
        pass


@bitmex.route("/settingValue", methods=['GET'])
def settingValue():
    try:
        user_id = current_user.id
        bitmex_settingValue = bitmex_mysqldb.settingValue(user_id)
        # print(res)
        return jsonify(bitmex_settingValue)
    except:
        pass

@bitmex.route("/onoff_Status", methods=['GET'])
def onoff_Status():
    try:
        user_id = current_user.id
        onoff_Status = bitmex_mysqldb.onoff_Status(user_id)
        return jsonify(onoff_Status)
    except:
        pass


@bitmex.route("/get_open_order", methods=['GET'])
def get_open_order():
    try:
        res = bitmex_Api.Api().get_open_order()
        # print(res)
        return jsonify(res)
    except:
        pass

@bitmex.route("/bitmex_bot_onoff", methods=['POST'])
def bitmex_bot_onoff():
    try:
        if request.method == 'POST':
            user_id = current_user.id
            onoff_Status = bitmex_mysqldb.botUpdate(user_id)
        return 'ok'
    except:
        pass

@bitmex.route("/bitmex_stoploss", methods=['POST'])
def bitmex_stoploss():
    try:
        if request.method == 'POST':
            user_id = current_user.id
            onoff_Status = bitmex_mysqldb.bitmex_stoploss(user_id)
        return 'ok'
    except:
        pass

@bitmex.route("/bitmex_appointment", methods=['POST'])
def bitmex_appointment():
    try:
        if request.method == 'POST':
            user_id = current_user.id
            onoff_Status = bitmex_mysqldb.bitmex_appointment(user_id)
        return 'ok'
    except:
        pass


@bitmex.route('/bitmex_buyintervalset', methods=['GET', 'POST'])
def bitmex_buyintervalset():
    try:
        user_id = current_user.id
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
            data = [buy_1, buy_2, buy_3, buy_4, buy_5, buy_6, buy_7, buy_8, buy_9]
            bitmex_mysqldb.buyintervalset(data, user_id)
        res = bitmex_mysqldb.buyintervalStatus(user_id)
        return jsonify(res)
    except:
        pass



@bitmex.route('/bitmex_settings', methods=['POST'])
def bitmex_settings():
    user_id = current_user.id
    if request.method == 'POST':
        print('bitmex_settings')
        start_payment = request.form['start_payment']
        count = request.form['count']
        entry_position = request.form['entry_position']
        positionsell = request.form['positionsell']
        loss_stop = request.form['loss_stop']
        currency = request.form['currency'].upper()
        data = [start_payment, count, positionsell, loss_stop, currency, entry_position]
        bitmex_mysqldb.setting_update(data, user_id)
        return 'ok'


@bitmex.route('/bitmex_cancelall', methods=['POST'])
@login_required
def bitmex_cancelall():
    print('bitmex_cancelall')
    if request.method == 'POST':
        bitmex_Api.Api().cancel_all('Buy')
        bitmex_Api.Api().cancel_all('Sell')
        bitmex_Api.Api().get_open_order()
        return "ok"


@bitmex.route('/bitmex_sellall', methods=['POST'])
@login_required
def bitmex_sellall():
    if request.method == 'POST':
        bitmex_Api.Api().position_close()
        return "ok"
    return "ok"


@bitmex.route('/bitmex_buyupdate', methods=['POST'])
@login_required
def bitmex_buyupdate():
    if request.method == 'POST':
        bitmex_Api.Api().buylist()
        return "ok"
    return "ok"


@bitmex.route('/bitmex_get_revenue')
def bitmex_get_revenue():
    res = bitmex_Api.Api().view_select_revenue() # [trade_vol, revenue, avg_price, avg_unit]
    return jsonify(res)


@bitmex.route('/bitmex_get_order_list')
def bitmex_get_order_list():
    getorders = bitmex_Api.Api().get_order_data()
    return jsonify(getorder=getorders)



@bitmex.route('/bitmex_apisetting', methods=['POST'])
def bitmex_apisetting():
    user_id = current_user.id
    print('bitmex_apisetting')
    connection = sqlsetting.mysqlset()
    if request.method == "POST":
        apikey = request.form['accessKey']
        secretKey = request.form['secretKey']
        bitmex = bitmexAPI.Bitmex(apikey, secretKey)
        data = bitmex.bitmex_my_balance()
        if "error" in data :
            print('error')
            return False
        else:
            print('apikey update')
            my_cursor = connection.cursor(pymysql.cursors.DictCursor)
            sql = '''update trade.bitmex_setting set apikey = %s, secretkey = %s where userid = %s'''
            my_cursor.execute(sql, (str(apikey), str(secretKey), user_id))
            connection.commit()

        connection.close()
        return 'POST'

    return 'GET'

@bitmex.route('/get_order_data')
def get_order_data():
    getorders = bitmex_Api.Api().get_order_data()
    return jsonify(getorder=getorders)