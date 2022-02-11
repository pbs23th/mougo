import time
import threading
import requests
import okex.consts as c
from . import okex_mysqldb
# import okex_mysqldb
import okex.Market_api as Market
import okex.Account_api as Account
import okex.Trade_api as Trade
from datetime import datetime
import decimal
from flask_login import current_user

def get_tick_size(price, step):
    try:
        ''' 호가단위 계산 '''
        tick_size = int(price / step) * decimal.Decimal(str(step))
        return float(tick_size)
    except Exception as e:
        print(e)
        print('okex_Api.get_tick_size error')
        return ""


def get_volume_size(unit, format):
    try:
        ''' 주문수량 자릿수 계산 '''
        volume_size = int(unit / format) * decimal.Decimal(str(format))
        return float(volume_size)
    except Exception as e:
        print(e)
        print('okex_Api.get_volume_size error')
        return ""



class Api:
    def __init__(self):
        self.user_id = str(current_user.id)
        okex_mysqldb2 = okex_mysqldb.settingValue(self.user_id)
        api_key = okex_mysqldb2['apikey']
        secret_key = okex_mysqldb2['secretkey']
        passphrase = okex_mysqldb2['passphrase']
        flag = '0'  # 实盘 real trading
        self.brokerid = okex_mysqldb2['brokerid']
        self.start_payment = okex_mysqldb2['start_payment']
        self.payment = okex_mysqldb2['payment']
        self.currency = okex_mysqldb2['currency']
        self.marketid = self.currency + '-' + self.payment
        self.count = okex_mysqldb2['count']
        self.positionsell = okex_mysqldb2['positionsell']
        self.loss_stop = okex_mysqldb2['loss_stop']
        instrument = okex_mysqldb.min_sz(self.marketid)
        self.minSz = float(instrument['minSz'])
        self.step = float(instrument['stepprice'])
        self.unitformat = float(instrument['unitformat'])

        self.accountAPI = Account.AccountAPI(api_key, secret_key, passphrase, False, flag)
        self.marketAPI = Market.MarketAPI(api_key, secret_key, passphrase, False, flag)
        self.tradeAPI = Trade.TradeAPI(api_key, secret_key, passphrase, False, flag)


    def _get_timestamp(self):
        try:
            '''브로커아이디 합성용 타임스탬프'''
            url = c.API_URL + c.SERVER_TIMESTAMP_URL
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()['data'][0]['ts']
            else:
                return ""
        except Exception as e:
            print(e)
            print('okex_Api.get_volume_size error ID : ',self.user_id)
            return ""


    def get_price(self):
        try:
            ''' 현재가 가져오기 '''
            ticker = self.marketAPI.get_ticker(self.marketid)
            ticker = float(ticker['data'][0]['last'])
            return ticker
        except Exception as e:
            print(e)
            print('okex_Api.get_price error ID : ',self.user_id)
            return ""


    # def insert_ordhistory(self):
    #     try:
    #         ''' 거래내역 조회후 저장 '''
    #         getorder = self.tradeAPI.get_orders_history(instType='SPOT', instId=self.marketid, state='filled', limit=100)
    #         getorder = getorder['data']
    #         okex_mysqldb.insert_data(getorder, self.user_id)
    #     except Exception as e:
    #         print(e)
    #         print('insert_ordhistory error ID : ',self.user_id)



    def cancelsell(self):
        print('okex-cancelsell ID : ',self.user_id, datetime.now())
        '''매도목록 취소'''
        try:
            getorder = self.tradeAPI.get_order_list(instType='SPOT', instId=self.marketid) #미채결목록확인
            getorder = getorder['data']
            if len(getorder) > 0:
                for i in getorder:
                    if i['side'] == 'sell':
                        cancelorder = self.tradeAPI.cancel_order(instId = self.marketid, ordId=i['ordId']) #취소주문
            else:
                pass
        except:
            print('okex-cancelsell error ID : ',self.user_id)


    def cancelbuy(self):
        print('okex-cancelbuy : ', datetime.now())
        '''매수목록 취소'''
        try:
            getorder = self.tradeAPI.get_order_list(instType='SPOT', instId=self.marketid) #미채결목록확인
            getorder = getorder['data']
            cancelbuylist = []
            if len(getorder) > 0:
                for i in getorder:
                    if i['side'] == 'buy':
                        cancelbuylist.append({"instId":self.marketid,"ordId":i['ordId']}) #오더아이디 저장
                if len(cancelbuylist) > 0:
                    cancelorder = self.tradeAPI.cancel_multiple_orders(cancelbuylist) #취소주문
            else:
                pass
        except:
            print('okex-cancelbuy error ID : ',self.user_id)


    def sellstatus(self):
        ''' 미채결 매도 수량확인'''
        try:
            getorder = self.tradeAPI.get_order_list(instType='SPOT', instId=self.marketid)
            getorder = getorder['data']
            asklist = []
            if len(getorder) > 0:
                for i in getorder:
                    if i['side'] == 'sell':
                        asklist.append(i)
                if len(asklist) > 0:
                    return asklist[0]
                else:
                    return {'sz' : 0 }
            else:
                return {'sz' : 0 }
        except:
            print('sellstatus error ID : ',self.user_id)
            return {'sz' : 0 }



    def sellupdate(self):
        try:
            print('okex-sellupdate : ', datetime.now())
            ''' 매도록목 상태 확인후 보유량과 미채결 양이 다를떄 매도주문 취소후 재주문'''
            cancel = self.cancelsell() # 매도 취소
            time.sleep(1)
            price2 = self.avg_price()  # 평단가 및 수량확인
            price = price2[2]  # 평단가 및 수량확인
            bal = self.accountAPI.get_account(self.currency)
            volume = float(bal['data'][0]['details'][0]['eq']) # 코인 보유수량 확인
            if volume > 0:
                price = get_tick_size(price*(1 + self.positionsell/100), self.step) # 매도가격 계산
                timestamp = self._get_timestamp()
                client_oid = self.brokerid + str(timestamp) # 브로커 id
                sellorder = self.tradeAPI.place_order(instId=self.marketid, tdMode='cash', side='sell', ordType='limit',
                                                      sz=volume, px=price, clOrdId=str(client_oid))
                print('okex-sellupdate sellorder: ', sellorder)
                if sellorder['code'] == '0':
                    ordId = sellorder['data'][0]['ordId']
                    self.ordid_insert(ordId)
                    self.select_ordidlist()
                return sellorder
            else:
                self.select_ordidlist()
        except:
            print('okex-sellupdate error ID : ',self.user_id)
#

    def avg_price(self):
        try:
            ''' 평단가 계산 마지막 매도 이후 매수목록 수집후 계산'''
            revenue2 = okex_mysqldb.select_orddata(self.marketid, self.user_id)
            vol = int(revenue2[1])
            revenue = revenue2[0]
            avgprice = get_tick_size(revenue2[2], self.step)
            return [revenue, vol, avgprice]
        except Exception as e:
            print(e)
            print('okex-avg_price error ID : ',self.user_id)


    def ordid_insert(self, ordId):
        try:
            print('okex-buylist : ', datetime.now())
            data = self.tradeAPI.get_orders(instId=self.marketid, ordId=ordId, clOrdId=None)
            if data['code'] == '0':
                okex_mysqldb.insert_ordid(data['data'][0], self.user_id)

            return data
        except Exception as e:
            print(e)
            print('okex-ordid_insert error ID : ',self.user_id)

    def resuch_ordid(self, data):
        try:
            canceled = []
            live = []
            filled = []
            not_exist = []
            if len(data) > 1:
                for i in data:
                    ordId = i['ordId']
                    filled_data = self.tradeAPI.get_orders(instId=self.marketid, ordId=ordId, clOrdId=None)
                    if filled_data['code'] != '51603':
                        state = filled_data['data'][0]['state']
                        ordId = filled_data['data'][0]['ordId']
                        if state == 'canceled':
                            if float(filled_data['data'][0]['fillSz']) > 0:
                                filled.append(filled_data['data'][0])
                            else:
                                canceled.append(filled_data['data'][0])
                        elif state == 'filled':
                            filled.append(filled_data['data'][0])
                        else:
                            live.append(ordId)
                    else:
                        not_exist.append(i)
                if len(filled) > 0:
                    okex_mysqldb.update_ordid(filled, 'filled')
                    okex_mysqldb.insert_data(filled, self.user_id)
                if len(canceled) > 0:
                    okex_mysqldb.update_ordid(canceled, 'canceled')
                if len(not_exist) > 0:
                    okex_mysqldb.update_ordid(not_exist, 'not_exist')

        except Exception as e:
            print(e)
            print('okex-resuch_ordid error ID : ', self.user_id)


    def select_ordidlist(self):
        try:
            ordlist = okex_mysqldb.select_ordid(self.marketid, self.user_id)
            self.resuch_ordid(ordlist)
        except Exception as e:
            print(e)
            print('okex-select_ordidlist error ID : ',self.user_id)


    def buylist(self):
        print('okex-buylist ID : ',self.user_id, datetime.now())
        ''' 매수목록 생성 '''
        try:
            self.cancelbuy() # 목록생성전 모든 매수주문 취소
            bal = self.accountAPI.get_account(self.payment+','+self.currency)
            bal2 = get_volume_size(float(bal['data'][0]['details'][1]['eq']),self.unitformat) #보유수량확인
            bal_order = get_volume_size(float(bal['data'][0]['details'][0]['eq'])-float(bal['data'][0]['details'][0]['ordFrozen']), self.unitformat) # 사용가능 USDT
            start_paymentsize = float(self.start_payment) * 2
            avgprice = okex_mysqldb.firstbuy_select(self.marketid, self.user_id) # 최초진입가격확인
            ticker = self.get_price()
            if avgprice > 0:
                buyset = okex_mysqldb.buyintervalstatus(self.user_id) # 매수목록생성 간격확인
                buysum = 0
                for i in range(self.count):
                    buysum += buyset[i]
                    per = (buysum/100)
                    price = avgprice - avgprice * per # 주문가격
                    orderprice = get_tick_size(price,self.step)
                    volume = start_paymentsize / orderprice
                    pricelist = []
                    if orderprice > ticker or bal2 > volume: # 주문가격이 현재가보다 높으면 패스
                        print('okex-orderprice > ticker : ', orderprice, ' > ', ticker, ' or ', 'bal2 > volume : ', bal2, ' > ', volume)
                    elif bal_order > start_paymentsize:
                        timestamp = self._get_timestamp()
                        client_oid = self.brokerid + str(timestamp)
                        sellorder = self.tradeAPI.place_order(instId=self.marketid, tdMode='cash', side='buy',
                                                              ordType='limit',
                                                              sz=volume, px=orderprice, clOrdId=str(client_oid))
                        if sellorder['code'] == '0':
                            ordId = sellorder['data'][0]['ordId']
                            self.ordid_insert(ordId)

                            bal_order = bal_order - volume*orderprice
                            pricelist.append(orderprice)
        #
                    else:
                        print('okex-lack of balance ID : ',self.user_id)
        # #
                    if i == self.count-1 and len(pricelist) > 0:
                        okex_mysqldb.lastorder_update(pricelist[-1], self.marketid, self.user_id)
                    start_paymentsize = start_paymentsize * 2
                    time.sleep(0.2)
            data = self.select_ordidlist()
        except Exception as e:
            print('e : ', e)
            print('okex-buylist error ID : ',self.user_id)
            time.sleep(1)
#

    def firstbuy(self):
        print('okex-firstbuy : ', datetime.now())
        try:
            self.select_ordidlist()
            self.cancelsell()
            self.cancelbuy()
            appointmentStatus = okex_mysqldb.appointmentStatus(self.user_id)
            if appointmentStatus == 'on':
                okex_mysqldb.botUpdate2(self.user_id)
                print('okex-end ID : ',self.user_id)
            else:
                timestamp = self._get_timestamp()
                client_oid = self.brokerid + str(timestamp)
                marketbuy = self.tradeAPI.place_order(instId=self.marketid, tdMode='cash', side='buy', ordType='market', sz=self.start_payment,  clOrdId=client_oid)
                print('okex-최초 주문  ID : ',self.user_id, marketbuy)
                if marketbuy['code'] == '0':
                    ordId = marketbuy['data'][0]['ordId']
                    data = self.ordid_insert(ordId)
                    okex_mysqldb.insert_data(data['data'], self.user_id)
                    okex_mysqldb.insert_ordid(data['data'][0], self.user_id)

                    while True:
                        print('get order history while start ID : ',self.user_id, datetime.now())
                        getorder = self.tradeAPI.get_orders_history(instType='SPOT', instId=self.marketid, state='filled', limit=1)

                        if marketbuy['data'][0]['ordId'] == getorder['data'][0]['ordId']:
                            break
                        time.sleep(1)
                    self.buylist()
                    self.sellupdate()
        except Exception as e:
           print(e)
           print('okex-firstbuy error ID : ',self.user_id)
#
#
#
    def sellposition(self):
        print('okex-sellposition ID : ',self.user_id, datetime.now())
        try:
            bal = self.accountAPI.get_account(self.currency)
            volume = get_volume_size(float(bal['data'][0]['details'][0]['eq']), self.unitformat)
            if volume > 0:
                timestamp = self._get_timestamp()
                client_oid = self.brokerid + str(timestamp)
                marketsell = self.tradeAPI.place_order(instId=self.marketid, tdMode='cash', side='sell', ordType='market',
                                                      sz=volume, clOrdId=client_oid)
                if marketsell['code'] == '0':
                    ordId = marketsell['data'][0]['ordId']
                    self.ordid_insert(ordId)
                    okex_mysqldb.insert_data(marketsell['data'], self.user_id)
                    okex_mysqldb.insert_ordid(marketsell['data'][0], self.user_id)

            self.select_ordidlist()

        except Exception as e:
            print(e)
            print('okex-sellposition error ID : ',self.user_id)
#
#
# #
    def run(self):
        print('start')
        data = self.select_ordidlist()
        print('start2')
        while True:
            try:
                bot = okex_mysqldb.botStatus(self.user_id)
                loss = okex_mysqldb.stoplossStatus(self.user_id)
                # self.insert_ordhistory()
                if bot == 'on':
                    print('okex-time : '+self.user_id, datetime.now())
                    vol = self.sellstatus()
                    bal = self.accountAPI.get_account(self.currency)
                    if len(bal['data'][0]['details']) > 0:
                        currency_bal = bal['data'][0]['details'][0]['eq']
                        bal2 = get_volume_size(float(bal['data'][0]['details'][0]['eq']), self.unitformat)
                        bal_order = get_volume_size(float(bal['data'][0]['details'][0]['ordFrozen']), self.unitformat)
                    else:
                        print('okex-NODATA')
                        bal2 = 0
                        bal_order = 0

                    if bal2 < float(self.minSz):
                        print('okex-currency_amount < minSz', self.minSz)
                        self.firstbuy()
                    elif bal2 == bal_order:
                        pass
                    else:
                        print('okex-run - sellupdate')
                        self.select_ordidlist()
                        time.sleep(1)
                        aaa = self.sellupdate()
                    ticker = self.get_price()
                    last_buyorder = okex_mysqldb.lastorder_select(self.marketid, self.user_id)
                    stoploss = last_buyorder - (last_buyorder*self.loss_stop)
                    if ticker < stoploss and loss == 'on':
                        print('okex-stop_loss')
                        cancel = self.cancelsell()
                        order = self.sellposition()
                else:
                    print('okex-while break')
                    break

            except Exception as e:
                # aaa = self.sellupdate()
                print('e: ',e)
                print('okex-run error ID : ',self.user_id)
                time.sleep(1)
            # bot = okex_mysqldb.botStatus()
            time.sleep(1)
#     def test(self):
#         while True:
#             print(datetime.now())
#             time.sleep(1)

class Worker(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        print("sub thread start ", threading.currentThread().getName())
        t = threading.Thread(target=Api().run())
        t.start()
        if t.is_alive() == True:
            print('ok')
        else:
            print('no')



# a = Api().buylist()
# a = Api().avg_price()
# print(a)
