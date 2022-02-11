import time
import threading
import requests
from datetime import datetime
import decimal
from flask_login import current_user
from . import bitmexAPI
from . import bitmex_mysqldb
# import bitmexAPI
# import bitmex_mysqldb
import pymysql
import datetime
import decimal




def get_tick_size(price):
    tick_size = int(price / 0.5) * decimal.Decimal(str(0.5))
    return float(tick_size)


def get_volume(volume):
    volume = int(volume * 100000000) * decimal.Decimal(str(0.00000001))
    return float(volume)


class Api:
    def __init__(self):
        self.user_id = str(current_user.id)
        setting_data = bitmex_mysqldb.settingValue(self.user_id)
        api_key = setting_data['apikey']
        secret_key = setting_data['secretkey']
        self.start_payment = setting_data['start_payment']/100
        self.payment = setting_data['payment']
        self.currency = setting_data['currency']
        self.marketid = self.currency
        self.count = setting_data['count']
        self.positionsell = setting_data['positionsell']/100
        self.entry_position = setting_data['entry_position']
        self.loss_stop = setting_data['loss_stop']/100
        self.minSz = 100
        self.step = float(0.5)
        self.unitformat = float(0.1)
        self.bitmex = bitmexAPI.Bitmex(api_key, secret_key)

    def set_startpay(self):
        multiple = 1
        num = 1
        ticker = self.get_price()
        wallet = self.wallet_balance()
        for i in range(self.count):
            num = num*2
            multiple += num

        start_orderpay = int(int(wallet*self.start_payment*ticker)/multiple/100)*100
        return start_orderpay


    def wallet_balance(self):
        res = self.bitmex.bitmex_my_balance(self.marketid)
        balance = res['walletBalance'] / 100000000
        bitmex_mysqldb.wallet_update(balance, self.user_id)
        return balance


    def get_balance(self):
        try:
            ''' 밸런스 가져오기 '''
            res = self.bitmex.bitmex_my_balance(self.marketid)
            balance = res['excessMargin']/100000000
            bitmex_mysqldb.balance_update(balance, self.user_id)
            return balance
        except Exception as e:
            print(e)
            print('bitmex_Api.get_price error ID : ',self.user_id)
            time.sleep(5)


    def get_price(self):
        try:
            ''' 현재가 가져오기 '''
            ticker = bitmex_mysqldb.get_ticker(self.marketid)
            return ticker
        except Exception as e:
            print(e)
            print('bitmex_Api.get_price error ID : ',self.user_id)
            return 0


    def avg_price(self):
        try:
            ''' 평단가 계산 마지막 매도 이후 매수목록 수집후 계산'''
            res = self.bitmex.bitmex_my_position(self.marketid)
            if res is None:
                res2 = self.bitmex.order_history(self.marketid)
                if len(res2) == 0:
                    avg_price = 0
                    avg_unit = 0
                else:
                    avg_price = None
                    avg_unit = None
                data = [avg_price, avg_unit]
            else:
                avg_price = res['avgEntryPrice']
                avg_unit = res['currentQty']
                data = [avg_price, avg_unit]
                bitmex_mysqldb.avg_update(data, self.user_id)
            return data
            # return None
        except Exception as e:
            print(e)
            print('bitmex-avg_price error ID : ',self.user_id)


    def market_buy(self, unit):
        print('bitmex-market_buy : ',self.user_id, datetime.datetime.now(),"  : unit = ",unit )
        unit = unit
        res = self.bitmex.bitmex_order(symbol=self.marketid, ordtype='market', buysell_side='Buy', orderQty=unit)
        bitmex_mysqldb.insert_ordid(res, self.user_id)
        return res


    def market_sell(self, unit):
        print('bitmex-market_sell : ',self.user_id, datetime.datetime.now(),"  : unit = ",unit )
        unit = unit
        res = self.bitmex.bitmex_order(symbol=self.marketid, ordtype='market', buysell_side='Sell', orderQty=unit)
        bitmex_mysqldb.insert_ordid(res, self.user_id)
        return res


    def limit_buy(self, price, unit):
        print('bitmex-limit_buy : ', self.user_id, datetime.datetime.now(), "  : price = ", price,", unit = ", unit)
        unit = abs(unit)
        price = price
        res = self.bitmex.bitmex_order(symbol=self.marketid, ordtype='limit', buysell_side='Buy', limit_price = price, orderQty=unit)
        bitmex_mysqldb.insert_ordid(res, self.user_id)
        return res


    def limit_sell(self, price, unit):
        print('bitmex-limit_sell : ', self.user_id, datetime.datetime.now(), "  : price = ", price,", unit = ", unit)
        unit = abs(unit)
        price = price
        res = self.bitmex.bitmex_order(symbol=self.marketid, ordtype='limit', buysell_side='Sell', limit_price = price, orderQty=unit)
        bitmex_mysqldb.insert_ordid(res, self.user_id)
        return res


    # def cancel_order(self, orderID):
    #     orderID = orderID
    #     res = self.bitmex.cancel_order(orderID)
    #     self.get_open_order()
    #     ''' 주문목록 업데이트'''
    #     return res


    def cancel_all(self, side):
        res = self.bitmex.cancel_all(self.marketid, side)
        self.get_open_order()
        ''' 주문목록 업데이트'''
        return res


    def insert_ordid(self, orderdata):
        res = bitmex_mysqldb.insert_ordid(orderdata, self.user_id)
        return res


    def select_ordid(self):
        res = bitmex_mysqldb.select_ordid(self.marketid, self.user_id)
        return res


    def view_select_revenue(self):
        data = bitmex_mysqldb.revenue_select(self.user_id)
        return data

    def view_balance(self):
        data2 = bitmex_mysqldb.balance_select(self.user_id)
        return data2


    def view_wallet(self):
        data2 = bitmex_mysqldb.wallet_select(self.user_id)
        return data2

    def select_revenue(self):
        try:
            res = bitmex_mysqldb.select_orddata(self.marketid, self.user_id) # [rate, trade_vol]
            avg = self.avg_price() # [avg_price, avg_unit]
            view_balance = self.view_balance()
            view_wallet = self.view_wallet()
            ticker = self.get_price()
            if avg[0] is None:
                avg_price = 0
                avg_unit = 0
            else:
                avg_price = avg[0]
                avg_unit = avg[1]
            revenue = res[0]
            trade_vol = res[1]
            if avg_unit != 0:
                revenue = get_volume(revenue-(avg_unit/avg_price))
            data = [trade_vol, revenue, avg_price, avg_unit, view_balance, ticker, view_wallet]
            bitmex_mysqldb.revenue_update(data, self.user_id)
            return data
        except Exception as e:
            print(e)
            print('select_revenue error')



    def buylist(self):
        ''' 매수목록 생성 '''
        try:
            if self.entry_position == 'long':
                print('buylist long', self.user_id)
                self.cancel_all('Buy')
                bal = self.avg_price()
                bal2 = bal[1] #보유수량확인
                ticker = self.get_price()
                bal_order = self.get_balance() * ticker * 2 # 사용가능 USDT
                start_paymentsize = int(self.set_startpay()) * 2
                avgprice = bitmex_mysqldb.firstbuy_select(self.marketid, self.user_id, self.entry_position) # 최초진입가격확인
                   
                if avgprice > 0 and bal2 > 0:
                    buyset = bitmex_mysqldb.buyintervalStatus(self.user_id) # 매수목록생성 간격확인
                    buysum = 0
                    pricelist = []
                    for i in range(self.count):
                        buysum += buyset[i]
                        per = (buysum/100)
                        price = avgprice - avgprice * per # 주문가격
                        orderprice = get_tick_size(price)
                        unit = start_paymentsize
                        if orderprice > ticker or bal2 > unit: # 주문가격이 현재가보다 높으면 패스
                            print('bitmex-orderprice > ticker : ', orderprice, ' > ', ticker, ' or ', 'bal2 > volume : ', bal2, ' > ', unit)
                        elif bal_order > start_paymentsize:
                            res = self.limit_buy(orderprice, unit)
                            print('limit_buy : ', res)
                            if 'error' not in res:        #
                                bal_order = bal_order - unit
                                pricelist.append(orderprice)
            # #
                        else:
                            print('bitmex-lack of balance ID : ',self.user_id)
                        if i == self.count-1 and len(pricelist) > 0:
                            bitmex_mysqldb.lastorder_update(pricelist[-1], self.marketid, self.user_id, self.entry_position)
                        start_paymentsize = start_paymentsize * 2
            else:
                print('buylist short', self.user_id)
                self.cancel_all('Sell')
                bal = self.avg_price()
                bal2 = bal[1]  # 보유수량확인
                ticker = self.get_price()
                bal_order = self.get_balance() * ticker * 2 # 사용가능 USDT
                start_paymentsize = int(self.set_startpay()) * 2
                avgprice = bitmex_mysqldb.firstbuy_select(self.marketid, self.user_id, self.entry_position)  # 최초진입가격확인
                if avgprice > 0 and abs(bal2) > 0:
                    buyset = bitmex_mysqldb.buyintervalStatus(self.user_id)  # 매수목록생성 간격확인
                    buysum = 0
                    pricelist = []
                    for i in range(self.count):
                        buysum += buyset[i]
                        per = (buysum / 100)
                        price = avgprice + avgprice * per  # 주문가격
                        orderprice = get_tick_size(price)
                        unit = start_paymentsize
                        if orderprice < ticker or abs(bal2) > abs(unit):  # 주문가격이 현재가보다 낮으면 패스
                            print('bitmex-orderprice > ticker : ', orderprice, ' < ', ticker, ' or ',
                                  'bal2 > volume : ', bal2, ' > ', unit)
                        elif bal_order > start_paymentsize:
                            res = self.limit_sell(orderprice, unit)
                            print('limit_sell : ', res)
                            if 'error' not in res:  #
                                bal_order = bal_order - unit
                                pricelist.append(orderprice)
                        # #
                        else:
                            print('bitmex-lack of balance ID : ', self.user_id)
                        if i == self.count - 1 and len(pricelist) > 0:
                            bitmex_mysqldb.lastorder_update(pricelist[-1], self.marketid, self.user_id, self.entry_position)
                        start_paymentsize = start_paymentsize * 2
            self.insert_orderhistory()
        except Exception as e:
            print('e : ', e)
            print('bitmex-buylist error ID : ',self.user_id)
            time.sleep(1)



    def first_buy(self):
        print('first_buy')
        self.wallet_balance()
        self.cancel_all('Buy')
        self.cancel_all('Sell')
        appointmentStatus = bitmex_mysqldb.onoff_Status(self.user_id)['appointment']
        if appointmentStatus == 'on':
            bitmex_mysqldb.botUpdate2(self.user_id)
            print('bitmex-end ID : ', self.user_id)
        else:
            if self.entry_position == 'long':
                res = self.market_buy(self.set_startpay())
                print('long : ', res)
            else:
                res = self.market_sell(self.set_startpay())
                print('short : ',res)
            if 'error' not in res:
                print('bitmex-최초 주문  ID : ', self.user_id, res)
                bitmex_mysqldb.insert_data([res], self.user_id)
                self.buylist()
                self.sell_update()


    def position_close(self):
        try:
            print('position_close')
            # self.cancel_all('Buy')
            # self.cancel_all('Sell')
            bal = self.avg_price()
            bal2 = bal[1]  # 보유수량확인
            if bal2 > 0:
                res = self.market_sell(abs(bal2))
            elif bal2 < 0:
                res = self.market_buy(abs(bal2))
            else:
                pass
            # res = self.bitmex.position_close(symbol=self.marketid)
            bitmex_mysqldb.insert_data([res], self.user_id)
            bitmex_mysqldb.insert_ordid(res, self.user_id)
            self.insert_orderhistory()
            self.get_balance()
            self.wallet_balance()
            self.select_revenue()

        except Exception as e:
            print(e)
            print('bitmex-position_close error ID : ',self.user_id)



    def sell_update(self):
        print('bitmex-sell_update : ' + self.user_id, datetime.datetime.now())
        if self.entry_position == 'long':
            self.cancel_all('Sell')
            res = self.avg_price()
            avg_price = res[0]
            unit = res[1]
            if unit < 0:
                pass
            else:
                per = 1 + self.positionsell
                sell_price = get_tick_size(avg_price*per)
                res = self.limit_sell(sell_price, unit)
        else:
            self.cancel_all('Buy')
            res = self.avg_price()
            avg_price = res[0]
            unit = res[1]
            if unit > 0:
                pass
            else:
                per = 1 - self.positionsell
                sell_price = get_tick_size(avg_price*per)
                res = self.limit_buy(sell_price, abs(unit))
        self.insert_orderhistory()


    def sell_status(self):
        try:
            res = self.get_order_data()
            if len(res) > 0:
                selllist = []
                if self.entry_position == 'long':
                    for i in res:
                        if i['side'] == 'Sell':
                            selllist.append(i)
                else:
                    for i in res:
                        if i['side'] == 'Buy':
                            selllist.append(i)
                if len(selllist) > 0:
                    return selllist[0]
                else:
                    return {'orderQty': 0}
            else:
                return {'orderQty': 0}

        except Exception as e:
            print(e)
            print('bitmex-sell_status error ID : ',self.user_id)
            return {'orderQty' : 0 }

        # avg_price = res[0]
        # unit = res[1]
        # per = (1 + (self.positionsell / 100))
        # sell_price = get_tick_size(avg_price*per, self.payment)
        # res = self.limit_sell(sell_price, unit)



    def get_order_data(self):
        open_order = bitmex_mysqldb.orderlist_select(self.user_id)
        return open_order


    def get_open_order(self):
        try:
            res = self.bitmex.open_order(self.marketid)
            if self.entry_position == 'long':
                res = sorted(res, key=lambda person: (float(person['price'])), reverse=True)
            else:
                res = sorted(res, key=lambda person: (float(person['price'])), reverse=False)
            if len(res) > 0:
                sum = 0
                for i in res:
                    sum += float(i['orderQty'])/float(i['price'])
                    i['sum'] = sum
                    i['XBT'] = float(i['orderQty'])/float(i['price'])
                    i['timestamp'] = str(datetime.datetime.strptime(str(i['timestamp']),'%Y-%m-%dT%H:%M:%S.%fZ') + datetime.timedelta(hours=9))
                res = sorted(res, key=lambda person: (float(person['price'])), reverse=True)
                open_order = res
                bitmex_mysqldb.orderlist_update(open_order, self.user_id)
                return res
            else:
                open_order = []
                bitmex_mysqldb.orderlist_update(open_order, self.user_id)
                return []
        except Exception as e:
            open_order = []
            bitmex_mysqldb.orderlist_update(open_order, self.user_id)
            print(e)
            return []


    def insert_orderhistory(self):
        try:
            ''' 거래내역 조회후 저장 '''
            orderid = self.select_ordid()
            order_id = []
            filled = []
            canceled = []
            new = []
            null_data = []
            for i in orderid:
                order_id.append(i['ordId'])
            res = self.bitmex.get_order(order_id)
            for i in res:
                if i['ordStatus'] == 'Canceled':
                    if i['cumQty'] > 0:
                        filled.append(i)
                    else:
                        canceled.append(i)
                elif i['ordStatus'] == 'Filled':
                    filled.append(i)
                elif i['ordStatus'] == 'New':
                    new.append(i)
                else:
                    null_data.append(i)
            if len(filled) > 0:
                bitmex_mysqldb.update_ordid(filled, 'Filled')
                bitmex_mysqldb.insert_data(filled, self.user_id)
            if len(canceled) > 0:
                bitmex_mysqldb.update_ordid(canceled, 'Canceled')
            if len(null_data) > 0:
                print('null_data : ', null_data)
        except Exception as e:
            print(e)
            print('insert_ordhistory error ID : ',self.user_id)


    def run(self):
        self.insert_orderhistory()
        self.wallet_balance()
        while True:
            try:
                status = bitmex_mysqldb.onoff_Status(self.user_id) # {'botstatus' : botstatus, 'stoploss_onoff' : stoploss_onoff, 'appointment' : appointment}
                bot = status['botstatus']
                loss = status['stoploss_onoff']
                self.get_open_order()
                self.select_revenue()
                ticker = self.get_price() # 현재가격
                if bot == 'on':
                    print('bitmex-time : '+self.user_id, datetime.datetime.now())
                    vol = self.sell_status()['orderQty'] # 미채결 매도주문상태
                    bal = self.get_balance()*ticker #사용가능 금액 USD 수량
                    currency_bal = self.avg_price() # [평단가, 포지션 진입수량]
                    bal_order = currency_bal[1]
                    if currency_bal[1] is None:
                        print('pass')
                        pass
                    else:
                        if currency_bal[1] == 0 and bal > 100 and currency_bal[1] is not None:
                            print('bitmex-currency_amount < minSz')
                            self.first_buy()
                        elif abs(vol) == abs(bal_order):
                            pass
                        else:
                            print('sell - update')
                            self.sell_update()
                        last_buyorder = bitmex_mysqldb.lastorder_select(self.marketid, self.user_id, self.entry_position)
                        if self.entry_position == 'long':
                            stoploss = last_buyorder - (last_buyorder*self.loss_stop)
                            if ticker < stoploss and loss == 'on':
                                print('bitmex-long-stop_loss')
                                self.position_close()
                        if self.entry_position == 'short':
                            stoploss = last_buyorder + (last_buyorder*self.loss_stop)
                            if ticker > stoploss and loss == 'on':
                                print('bitmex-short-stop_loss')
                                self.position_close()
                else:

                    print('bitmex-while break')
                    break
#
            except Exception as e:
                print('e: ',e)
                print('bitmex-run error ID : ',self.user_id)
                time.sleep(1)
            time.sleep(4)

#
class Worker(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        print("sub thread start ", threading.currentThread().getName())
        t = threading.Thread(target=Api().run())
        if t.is_alive() == True:
            print('is_alive')
        else:
            t.start()
            print('start')
#
# Api().run()
# Api().position_close()