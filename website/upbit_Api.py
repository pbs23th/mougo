import pyupbit
import time
from . import upbit_mysqldb
# import upbit_mysqldb
import threading
from datetime import datetime
from flask_login import current_user

def get_tick_size(price, payment):
    if payment == 'KRW':
        if price >= 2000000:
            tick_size = int(price / 1000) * 1000
        elif price >= 1000000:
            tick_size = int(price / 500) * 500
        elif price >= 500000:
            tick_size = int(price / 100) * 100
        elif price >= 100000:
            tick_size = int(price / 50) * 50
        elif price >= 10000:
            tick_size = int(price / 10) * 10
        elif price >= 1000:
            tick_size = int(price / 5) * 5
        elif price >= 100:
            tick_size = int(price / 1) * 1
        elif price >= 10:
            tick_size = int(price / 0.1) / 10
        elif price >= 1:
            tick_size = int(price / 0.01) / 100
        else:
            tick_size = int(price / 0.001) / 1000
    else:
        tick_size = int(price / 0.00000001) / 100000000
    return tick_size



class Api:
    def __init__(self):
        self.user_id = str(current_user.id)
        upbit_mysqldb2 = upbit_mysqldb.settingValue(self.user_id)
        access_key = upbit_mysqldb2['apikey']
        secret_key = upbit_mysqldb2['secretkey']
        self.start_payment = upbit_mysqldb2['start_payment']
        self.payment = upbit_mysqldb2['payment']
        self.currency = upbit_mysqldb2['currency']
        self.marketid = self.payment + '-' + self.currency
        self.count = upbit_mysqldb2['count']
        self.positionsell = upbit_mysqldb2['positionsell']
        self.loss_stop = (upbit_mysqldb2['loss_stop']/100)

        self.upbit = pyupbit.Upbit(access_key, secret_key)


    def get_price(self):
        try:
            ''' 현재가 가져오기 '''
            ticker = pyupbit.get_current_price(self.payment + '-' + self.currency)
            return ticker
        except Exception as e:
            print(e)
            print('upbit_Api.get_price error ID : ',self.user_id)
            return ""


    def cancelsell(self):
        try:
            ''' 매도주문 취소 '''
            print('upbit-cancelsell  ID : ',self.user_id, datetime.now())
            getorder = self.upbit.get_order(self.payment + '-' + self.currency, state='wait')
            if len(getorder) > 0:
                for i in getorder:
                    if i['side'] == 'ask':
                        self.upbit.cancel_order(i['uuid'])
            else:
                pass
        except Exception as e:
            print(e)
            print('upbit-cancelsell error ID : ',self.user_id)


    def cancelbuy(self):
        try:
            ''' 매수주문 취소'''
            print('upbit-cancelbuy ID : ',self.user_id, datetime.now())
            getorder = self.upbit.get_order(self.payment + '-' + self.currency, state='wait')
            if len(getorder) > 0:
                for i in getorder:
                    if i['side'] == 'bid':
                        self.upbit.cancel_order(i['uuid'])
            else:
                pass
        except Exception as e:
            print(e)
            print('upbit - cancelbuy error ID : ',self.user_id)


    def sellstatus(self):
        try:
            ''' 매도주문 조회'''
            getorder = self.upbit.get_order('KRW-' + self.currency, state='wait')
            asklist = []
            if len(getorder) > 0:
                for i in getorder:
                    if i['side'] == 'ask':
                        asklist.append(i)
                if len(asklist) > 0:
                    return asklist[0]
            else:
                return {'volume' : 0 }
        except Exception as e:
            print(e)
            print('upbit-sellstatus error ID : ',self.user_id)
            return {'volume' : 0 }



    def sellupdate(self):
        try:
            ''' 매도주문 취소후 새로 주문'''
            print('upbit-sellupdate  ID : ',self.user_id, datetime.now())
            cancel = self.cancelsell()
            volume = self.upbit.get_balance(self.currency)
            if volume > 0:
                price = get_tick_size(self.avg_price()*(1 + self.positionsell/100), self.payment)
                sellorder = self.upbit.sell_limit_order(self.payment + '-' + self.currency, price, volume)
                if 'error' in sellorder:
                    print('error  ID : ',self.user_id)
                else:
                    uuid = sellorder['uuid']
                    self.ordid_insert(uuid)
            self.select_ordidlist()
        except Exception as e:
            print(e)
            print('upbit-sellupdate error ID : ',self.user_id)


    def avg_price(self):
        try:
            ''' 평단가 조회'''
            avgprice = get_tick_size(self.upbit.get_avg_buy_price(self.currency), self.payment)
            return avgprice
        except Exception as e:
            print(e)
            print('upbit-avg_price error ID : ',self.user_id)


    def revenue(self):
        try:
            ''' 수익 거래량 계산'''
            revenue2 = upbit_mysqldb.select_orddata(self.marketid, self.user_id)
            vol = int(revenue2[1])
            revenue = revenue2[0]
            return [revenue, vol]
        except Exception as e:
            print(e)
            print('upbit-revenue error ID : ',self.user_id)



    def ordid_insert(self, uuid):
        try:
            ''' 주문내역 저장'''
            print('upbit-buylist ID : ',self.user_id, datetime.now())
            data = self.upbit.get_order(uuid)
            if 'error' not in data:
                upbit_mysqldb.insert_ordid(data, self.user_id)
        except Exception as e:
            print(e)
            print('upbit-buylist error ID : ',self.user_id)


    def resuch_ordid(self, data):
        try:
            ''' 주문내역 개별조회 / 상태분류'''
            canceled = []
            live = []
            filled = []
            if len(data) > 0:
                for i in data:
                    ordId = i['ordId']
                    filled_data = self.upbit.get_order(ordId)
                    state = filled_data['state']
                    # uuid = filled_data['uuid']
                    if state == 'cancel':
                        if len(filled_data['trades']) > 0:
                            filled.append(filled_data)
                        else:
                            canceled.append(filled_data)
                    elif state == 'done':
                        filled.append(filled_data)
                    else:
                        live.append(ordId)
                if len(filled) > 0:
                    upbit_mysqldb.update_ordid(filled, 'filled')
                    upbit_mysqldb.insert_data(filled, self.user_id)
                if len(canceled) > 0:
                    upbit_mysqldb.update_ordid(canceled, 'canceled')

        except Exception as e:
            print(e)
            print('upbit-resuch_ordid error ID : ',self.user_id)


    def select_ordidlist(self):
        try:
            ''' 주문내역리스트 조회'''
            ordlist = upbit_mysqldb.select_ordid(self.marketid, self.user_id)
            self.resuch_ordid(ordlist)

        except Exception as e:
            print(e)
            print('upbit-select_ordidlist error ID : ',self.user_id)



    def buylist(self):
        try:
            ''' 매수주문 목록 생성 '''
            print('upbit-buylist ID : ',self.user_id, datetime.now())
            self.cancelbuy()
            # avgprice = pyupbit.get_current_price(self.payment + '-' + self.currency)
            bal = self.upbit.get_balance_t(self.currency)
            bal_order = self.upbit.get_balance(self.payment)
            start_paymentsize = float(self.start_payment) * 2
            avgprice = upbit_mysqldb.firstbuy_select(self.marketid, self.user_id)
            ticker = self.get_price()
            if avgprice > 0:
                buyset = upbit_mysqldb.buyintervalstatus(self.user_id)
                buysum = 0
                for i in range(self.count):
                    buysum += buyset[i]
                    per = (buysum / 100)
                    price = avgprice - avgprice * per
                    orderprice = get_tick_size(price, self.payment)
                    volume = start_paymentsize / orderprice
                    if bal > volume or price > ticker:
                        print('upbit-bal > volume or price > ticker')
                    elif bal_order > start_paymentsize:
                        orders = self.upbit.buy_limit_order(self.payment + '-' + self.currency, orderprice, volume)
                        print('upbit-orders  ID : ',self.user_id, orders)
                        if 'error' not in orders:
                            ordId = orders['uuid']
                            self.ordid_insert(ordId)
                    #
                    else:
                        print('upbit-lack of balance ID : ',self.user_id)
                    #
                    if i == self.count - 1:
                        print('last ID : ',self.user_id)
                        getorder = self.upbit.get_order(self.payment + '-' + self.currency, state='wait')
                        if len(getorder) > 0:
                            for i in getorder:
                                if i['side'] == 'bid':
                                    upbit_mysqldb.lastorder_update(i['price'], self.marketid, self.user_id)
                                    break
                    start_paymentsize = start_paymentsize * 2
                    time.sleep(0.2)
            self.select_ordidlist()
        except Exception as e:
            print('e : ', e)
            print('upbit-buylist error ID : ',self.user_id)
            time.sleep(1)


    def firstbuy(self):
        try:
            ''' 밸런스가 0 일때 하는 최초 매수주문 시장가 매수'''
            print('upbit-firstbuy : ', datetime.now())
            self.cancelsell()
            self.cancelbuy()
            appointmentStatus = upbit_mysqldb.appointmentStatus(self.user_id)
            if appointmentStatus == 'on':
                upbit_mysqldb.botUpdate2(self.user_id)
                print('upbit-end ID : ',self.user_id)
            else:
                marketbuy = self.upbit.buy_market_order(self.payment + '-' + self.currency, self.start_payment)
                print('upbit-최초 주문  ID : ',self.user_id, marketbuy)
                time.sleep(1)
                if 'error' in marketbuy:
                    print('error ID : ',self.user_id)
                else:
                    uuid = marketbuy['uuid']
                    self.ordid_insert(uuid)
                    getorder = self.upbit.get_order(uuid)
                    print('-------------------------------------------------')
                    print(getorder)
                    upbit_mysqldb.insert_data([getorder], self.user_id)
                    upbit_mysqldb.insert_ordid(marketbuy, self.user_id)
                    self.select_ordidlist()
                self.buylist()
                self.sellupdate()

        except Exception as e:
           print(e)
           print('upbit-firstbuy error ID : ',self.user_id)



    def sellposition(self):
        try:
            ''' 보유코인 모두 시장가 매도'''
            print('upbit-sellposition ID : ',self.user_id, datetime.now())
            volume = self.upbit.get_balance(self.currency)
            if volume > 0:
                marketsell = self.upbit.sell_market_order(self.payment + '-' + self.currency, volume)
                if 'error' in marketsell:
                    print('error ID : ',self.user_id)
                else:
                    uuid = marketsell['uuid']
                    self.ordid_insert(uuid)
                    upbit_mysqldb.insert_data([marketsell], self.user_id)
                    upbit_mysqldb.insert_ordid(marketsell, self.user_id)
            self.select_ordidlist()

        except Exception as e:
            print(e)
            print('upbit-sellposition error ID : ',self.user_id)


# 
    def run(self):
        self.select_ordidlist()
        ''' 루프 시작 '''
        while True:
            try:
                bot = upbit_mysqldb.botStatus(self.user_id)
                loss = upbit_mysqldb.stoplossStatus(self.user_id)
                if bot == 'on':
                    print('upbit-time ID : ',self.user_id, datetime.now())
                    vol = self.sellstatus()
                    currency_amount = self.upbit.get_amount(self.currency)
                    bal = self.upbit.get_balance_t(self.currency)
                    if currency_amount < 4000:
                        self.firstbuy()
                    elif float(bal) == float(vol['volume']):
                        pass
                    else:
                        print('upbit-run - sellupdate ID : ',self.user_id)
                        aaa = self.sellupdate()
                    ticker = self.get_price()
                    last_buyorder = upbit_mysqldb.lastorder_select(self.marketid, self.user_id)
                    stoploss = last_buyorder - (last_buyorder*self.loss_stop)
                    if ticker < stoploss and loss == 'on':
                        print(ticker, ' ', stoploss)
                        print('upbit-stop_loss ID : ',self.user_id)
                        cancel = self.cancelsell()
                        order = self.sellposition()


                else:
                    print('upbit-while break ID : ',self.user_id)
                    break
                self.select_ordidlist()

            except Exception as e:
                # aaa = self.sellupdate()
                print('e: ',e)
                print('upbit-run error ID : ',self.user_id)
                time.sleep(1)
            # bot = upbit_mysqldb.botStatus()
            time.sleep(1)


class Worker(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        ''' 쓰래드 시작'''
        print("sub thread start ", threading.currentThread().getName())
        t = threading.Thread(target=Api().run())
        t.start()

