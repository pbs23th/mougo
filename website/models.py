from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

''' 유저정보 '''
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150))
    password = db.Column(db.String(150))



class Api_key(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    exchange = db.Column(db.String(45))
    access_key = db.Column(db.String(150), unique=True)
    secret_key = db.Column(db.String(150))
    passphrase = db.Column(db.String(45))
    user_id = db.Column(db.Integer)

''' okex '''


class okex_instrument(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    baseCcy = db.Column(db.String(45))
    category = db.Column(db.String(45))
    instId = db.Column(db.String(45))
    instType = db.Column(db.String(45))
    lever = db.Column(db.String(45))
    listTime = db.Column(db.String(45))
    lotSz = db.Column(db.String(45))
    minSz = db.Column(db.String(45))
    quoteCcy = db.Column(db.String(45))
    state = db.Column(db.String(45))
    tickSz = db.Column(db.String(45))


#
# ''' buyintervalset '''
# class Okex_buyintervalset(db.Model):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     buy_1 = db.Column(db.Float)
#     buy_2 = db.Column(db.Float)
#     buy_3 = db.Column(db.Float)
#     buy_4 = db.Column(db.Float)
#     buy_5 = db.Column(db.Float)
#     buy_6 = db.Column(db.Float)
#     buy_7 = db.Column(db.Float)
#     buy_8 = db.Column(db.Float)
#     buy_9 = db.Column(db.Float)
#     userid = db.Column(db.Integer)
#
#
# class Upbit_buyintervalset(db.Model):
#     id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
#     buy_1 = db.Column(db.Float)
#     buy_2 = db.Column(db.Float)
#     buy_3 = db.Column(db.Float)
#     buy_4 = db.Column(db.Float)
#     buy_5 = db.Column(db.Float)
#     buy_6 = db.Column(db.Float)
#     buy_7 = db.Column(db.Float)
#     buy_8 = db.Column(db.Float)
#     buy_9 = db.Column(db.Float)
#     userid = db.Column(db.Integer)
#
#
# class bitmex_buyintervalset(db.Model):
#     id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
#     buy_1 = db.Column(db.Float)
#     buy_2 = db.Column(db.Float)
#     buy_3 = db.Column(db.Float)
#     buy_4 = db.Column(db.Float)
#     buy_5 = db.Column(db.Float)
#     buy_6 = db.Column(db.Float)
#     buy_7 = db.Column(db.Float)
#     buy_8 = db.Column(db.Float)
#     buy_9 = db.Column(db.Float)
#     userid = db.Column(db.Integer)


''' orderhistory '''
class okex_orderhistory(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    order_time = db.Column(db.DateTime)
    market = db.Column(db.String(150))
    side = db.Column(db.String(45))
    price = db.Column(db.Float)
    unit = db.Column(db.Float)
    fee = db.Column(db.Float)
    ordertype = db.Column(db.String(45))
    orderstate = db.Column(db.String(45))
    transact_time = db.Column(db.DateTime)
    userid = db.Column(db.Integer)
    ordId = db.Column(db.String(150), unique=True)
    remaining_volume = db.Column(db.Float)
    last_order = db.Column(db.Float)


class upbit_orderhistory(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    order_time = db.Column(db.DateTime)
    market = db.Column(db.String(150))
    side = db.Column(db.String(45))
    price = db.Column(db.Float)
    unit = db.Column(db.Float)
    fee = db.Column(db.Float)
    ordertype = db.Column(db.String(45))
    orderstate = db.Column(db.String(45))
    transact_time = db.Column(db.DateTime)
    userid = db.Column(db.Integer)
    ordId = db.Column(db.String(150), unique=True)
    remaining_volume = db.Column(db.Float)
    last_order = db.Column(db.Float)


class bitmex_orderhistory(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    order_time = db.Column(db.DateTime)
    market = db.Column(db.String(150))
    side = db.Column(db.String(45))
    price = db.Column(db.Float)
    unit = db.Column(db.Float)
    fee = db.Column(db.Float)
    ordertype = db.Column(db.String(45))
    orderstate = db.Column(db.String(45))
    transact_time = db.Column(db.DateTime)
    userid = db.Column(db.Integer)
    ordId = db.Column(db.String(150), unique=True)
    remaining_volume = db.Column(db.Float)
    last_order = db.Column(db.Float)



''' 주문내역 '''
class okex_ordidlist(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    time = db.Column(db.DateTime)
    market = db.Column(db.String(45))
    ordId = db.Column(db.String(150))
    userid = db.Column(db.Integer)
    state = db.Column(db.String(45))


class upbit_ordidlist(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    time = db.Column(db.DateTime)
    market = db.Column(db.String(45))
    ordId = db.Column(db.String(150))
    userid = db.Column(db.Integer)
    state = db.Column(db.String(45))


class bitmex_ordidlist(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    time = db.Column(db.DateTime)
    market = db.Column(db.String(45))
    ordId = db.Column(db.String(150))
    userid = db.Column(db.Integer)
    state = db.Column(db.String(45))


#
# ''' 셋팅 '''
# class Okex_setting(db.Model):
#     id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
#     apikey = db.Column(db.String(150))
#     secretkey = db.Column(db.String(150))
#     start_payment = db.Column(db.Float)
#     currency = db.Column(db.String(45))
#     botstatus = db.Column(db.Integer)
#     count = db.Column(db.Integer)
#     positionsell = db.Column(db.Float)
#     payment = db.Column(db.String(45))
#     loss_stop = db.Column(db.Float)
#     stoploss_onoff = db.Column(db.Float)
#     passphrase = db.Column(db.String(45))
#     brokerid = db.Column(db.String(45))
#     stepprice = db.Column(db.String(45))
#     unitformat = db.Column(db.String(45))
#     appointment = db.Column(db.Integer)
#     entry_position = db.Column(db.String(45))
#     userid = db.Column(db.Integer, unique=True)
#
#
# class Upbit_setting(db.Model):
#     id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
#     apikey = db.Column(db.String(150))
#     secretkey = db.Column(db.String(150))
#     start_payment = db.Column(db.Float)
#     currency = db.Column(db.String(45))
#     botstatus = db.Column(db.Integer)
#     count = db.Column(db.Integer)
#     positionsell = db.Column(db.Float)
#     payment = db.Column(db.String(45))
#     loss_stop = db.Column(db.Float)
#     stoploss_onoff = db.Column(db.Float)
#     passphrase = db.Column(db.String(45))
#     brokerid = db.Column(db.String(45))
#     stepprice = db.Column(db.String(45))
#     unitformat = db.Column(db.String(45))
#     appointment = db.Column(db.Integer)
#     entry_position = db.Column(db.String(45))
#     userid = db.Column(db.Integer, unique=True)
#
#
# class bitmex_setting(db.Model):
#     id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
#     apikey = db.Column(db.String(150))
#     secretkey = db.Column(db.String(150))
#     start_payment = db.Column(db.Float)
#     currency = db.Column(db.String(45))
#     botstatus = db.Column(db.Integer)
#     count = db.Column(db.Integer)
#     positionsell = db.Column(db.Float)
#     payment = db.Column(db.String(45))
#     loss_stop = db.Column(db.Float)
#     stoploss_onoff = db.Column(db.Float)
#     passphrase = db.Column(db.String(45))
#     brokerid = db.Column(db.String(45))
#     stepprice = db.Column(db.String(45))
#     unitformat = db.Column(db.String(45))
#     appointment = db.Column(db.Integer)
#     entry_position = db.Column(db.String(45))
#     userid = db.Column(db.Integer, unique=True)


class bot_setting(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    apikey = db.Column(db.String(150))
    secretkey = db.Column(db.String(150))
    start_payment = db.Column(db.Float)
    currency = db.Column(db.String(45))
    botstatus = db.Column(db.Integer)
    count = db.Column(db.Integer)
    positionsell = db.Column(db.Float)
    payment = db.Column(db.String(45))
    loss_stop = db.Column(db.Float)
    stoploss_onoff = db.Column(db.Float)
    passphrase = db.Column(db.String(45))
    brokerid = db.Column(db.String(45))
    stepprice = db.Column(db.String(45))
    unitformat = db.Column(db.String(45))
    appointment = db.Column(db.Integer)
    entry_position = db.Column(db.String(45))
    userid = db.Column(db.Integer, unique=True)
    bot_id = db.Column(db.Integer, unique=True)


class buyintervalset(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    buy_1 = db.Column(db.Float)
    buy_2 = db.Column(db.Float)
    buy_3 = db.Column(db.Float)
    buy_4 = db.Column(db.Float)
    buy_5 = db.Column(db.Float)
    buy_6 = db.Column(db.Float)
    buy_7 = db.Column(db.Float)
    buy_8 = db.Column(db.Float)
    buy_9 = db.Column(db.Float)
    bot_id = db.Column(db.Integer)
