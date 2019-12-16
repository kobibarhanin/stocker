from alpha_vantage.timeseries import TimeSeries
URL = "https://www.alphavantage.co/query"


class DataSet:

    def __init__(self, symbol, resolution='1min'):
        ts = TimeSeries(key='DZ91XGSZEHIR84PX')
        self.data, metadata = ts.get_intraday(symbol, interval=resolution, outputsize='full')

    def __len__(self):
        return len(self.data)


class Stock:

    def __init__(self, symbol, data_set) -> None:

        self.symbol = symbol
        self.data_set = data_set.data
        self.amount = 0
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
        self.sell_point = avg + self.pred_growth
        self.sell_point = self.sell_point * 1.02

        # - buy when in low
        self.buy_point = self.min_price + self.pred_growth
        self.buy_point = self.buy_point * 0.98

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

    msft_data = DataSet('MSFT')
    panw_data = DataSet('PANW')
    aapl_data = DataSet('AAPL')

    msft_stock = Stock('MSFT', msft_data)
    panw_stock = Stock('PANW', panw_data)
    aapl_stock = Stock('AAPL', aapl_data)

    msft_stock.calculate_parameters()
    panw_stock.calculate_parameters()
    aapl_stock.calculate_parameters()

    msft_stock.print_info()
    panw_stock.print_info()
    aapl_stock.print_info()

    stocks = [msft_stock,panw_stock,aapl_stock]

    trial_length = min([len(msft_data),len(panw_data),len(aapl_data)])

    start_with = 10000
    funds = start_with

    for i in range(trial_length):
        # print(f'iteration = {i}')
        for stock in stocks:

            price = float(stock.data_set[stock.rev_keys[i]]['4. close'])
            # print(f'price = {price}')

            if stock.is_a_sell(price) and stock.amount > 0:
                print(f'selling at price = {price}, with stocks = {stock.amount}')
                funds += stocks * price
                stock.amount = 0
                print(f' - after sell: funds = {funds}, stocks = {stock.amount}')

            if stock.is_a_buy(price) and funds > price:
                print(f'buying at price = {price}, with funds = {funds}')
                while funds > price:
                    funds -= price
                    stock.amount += 1
                print(f' - after buy: funds = {funds}, stocks = {stock.amount}')

    value = funds
    value += funds + msft_stock.amount * msft_stock.last_price
    value += funds + panw_stock.amount * panw_stock.last_price
    value += funds + aapl_stock.amount * aapl_stock.last_price
    print(f'=========================================')
    print(f'value = {value}')
