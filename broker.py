import time
import datetime

from alpha_vantage.timeseries import TimeSeries
URL = "https://www.alphavantage.co/query"

import pymongo
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['stocker']
stocks_coll = db['stocks']
settings_coll = db['settings']
transactions_coll = db['transactions']


class DataSet:

    def __init__(self, symbol, resolution='1min'):
        ts = TimeSeries(key='DZ91XGSZEHIR84PX')
        self.data, metadata = ts.get_intraday(symbol, interval=resolution, outputsize='full')

    def __len__(self):
        return len(self.data)


class Stock:

    def __init__(self, symbol, data_set, amount=0) -> None:

        self.symbol = symbol
        self.data_set = data_set.data
        self.amount = amount
        self.rev_keys = list(data_set.data.keys())
        self.rev_keys.reverse()


    def is_a_buy(self, current_price):
        return current_price < self.buy_point

    def is_a_sell(self, current_price):
        return current_price > self.sell_point

    def calculate_parameters(self, sample_size=0):

        calc_keys = list(self.data_set.keys())[sample_size:]

        total = 0
        prices = []

        calc_keys = calc_keys[0:len(calc_keys)//2]

        for key in calc_keys:
            total += float(self.data_set[key]['4. close'])
            prices.append(float(self.data_set[key]['4. close']))

        avg = total / len(calc_keys)

        self.last_day = calc_keys[0]
        self.first_day = calc_keys[-1]

        self.first_price = float(self.data_set[self.first_day]["4. close"])
        self.last_price = float(self.data_set[self.last_day]["4. close"])

        self.max_price = max(prices)
        self.min_price = min(prices)

        self.growth = self.last_price / self.first_price - 1
        self.pred_growth = avg * self.growth

        # - sell when in peak
        self.sell_point = avg + self.pred_growth * 0.7
        # self.sell_point = self.sell_point * 1.02

        # - buy when in low
        self.buy_point = self.min_price + self.pred_growth * 1.2
        # self.buy_point = self.buy_point * 0.98

        self.aptitude = 0
        for i in range(10):
            curr_val = float(self.data_set[calc_keys[i]]['4. close'])
            former_val = float(self.data_set[calc_keys[i+1]]['4. close'])
            self.aptitude += curr_val-former_val



    def print_info(self):

        print(f'=== {self.symbol} ===')
        print(f'first_price = {self.first_price} at {self.first_day}')
        print(f'last_price = {self.last_price} at {self.last_day}')
        print(f'max_price = {self.max_price}')
        print(f'min_price = {self.min_price}')
        print(f'growth = {self.growth}')
        print(f'sell_point = {self.sell_point}')
        print(f'buy_point = {self.buy_point}')
        print(f'==============')


if __name__ == '__main__':

    stocks = []
    stocks_sample_size = []
    for stock_ent in stocks_coll.find():
        print(stock_ent)
        data = DataSet(stock_ent['symbol'])
        stock = Stock(stock_ent['symbol'], data, stock_ent['amount'])
        stock.calculate_parameters()
        stocks.append(stock)
        stock.print_info()
        stocks_sample_size.append(len(data))
        time.sleep(13)

    stocks.sort(key=lambda x: x.aptitude, reverse=False)
    trial_length = min(stocks_sample_size)

    start_with = settings_coll.find_one({'name': 'funds'})['total']
    funds = start_with

    for stock in stocks:

        price = float(stock.last_price)

        if stock.is_a_sell(price) and stock.amount > 0:
            transaction = f'selling {stock.symbol} at price = {price}, with stocks = {stock.amount}'
            transactions_coll.insert_one({'time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'transaction':transaction})
            print(transaction)

            funds += stock.amount * price
            stock.amount = 0
            print(f' - after sell: funds = {funds}, stocks = {stock.amount}')

        if stock.is_a_buy(price):
            if funds > price:
                transaction = f'buying {stock.symbol} at price = {price}, with funds = {funds}'
                transactions_coll.insert_one({'time':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'transaction':transaction})
                print(transaction)

                while funds > price:
                    funds -= price
                    stock.amount += 1
                print(f' - after buy: funds = {funds}, stocks = {stock.amount}')
            else:
                transaction = f'No buy of {stock.symbol} - LACK OF FUNDS - at {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
#                transactions_coll.insert_one({'time':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'transaction':transaction})

    value = funds
    for stock in stocks:
        stocks_coll.update({'symbol': stock.symbol}, {'$set': {'amount': stock.amount}})
        value += stock.amount * stock.last_price

    settings_coll.update({'name': 'funds'}, {'$set': {'total': funds}})
    settings_coll.update({'name': 'value'}, {'$set': {'total': value}})

    print(f'=========================================')
    print(f'value = {value}')
