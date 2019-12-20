# get_stock_value('MSFT')


# print(f'value = {simulate_stocks()}')

# SYMBOLS = ['PANW',
#            'MSFT',
#            'AAPL']
#            # 'GOOGL',
#            # 'AMZN',
#            # 'FB',
#            # 'BABA',
#            # 'NVDA',
#            # 'PYPL',
#            # 'TSLA',
#            # 'INTC']
#
# RESOLUTIONS = ['1min', '60min']
#
# results = dict()
#
# i = 1
# for symbol in SYMBOLS:
#     if (i % 4) == 0:
#         import time
#         time.sleep(80)
#
#     sys.stdout.write('* ')
#     # blockPrint()
#     results[symbol] = simulate_earnings(symbol, '1min')
#     # enablePrint()
#
#     i += 1
#
# sorted_results = sorted(results.items(), key=operator.itemgetter(1),reverse=True)
# print()
# print(sorted_results)


def simulate_earnings(symbol, resolution):

    stock = Stock(symbol, resolution)
    stock.print_info()

    # blockPrint()
    print(f'========== Trial ==========')
    start_with = 10000
    funds = start_with
    stocks = 0
    iteration = 0
    for time, point in stock.data_set.items():
        print(f'iteration = {iteration}')
        price = float(point['4. close'])
        if price < stock.buy_point and funds > price:
            print(f'buying at price = {price}, with funds = {funds}')
            while funds > price:
                funds -= price
                stocks += 1
            print(f' - after buy: funds = {funds}, stocks = {stocks}')
        else:
            print(f'passing buy at price = {price}')
        if price > stock.sell_point and stocks > 0:
            print(f'selling at price = {price}, with stocks = {stocks}')
            funds += stocks*price
            stocks = 0
            print(f' - after sell: funds = {funds}, stocks = {stocks}')
        else:
            print(f'passing sell at price = {price}')
        iteration += 1
        print(f'=====================================================')
    # enablePrint()

    print(f'stocks = {stocks}')
    print(f'funds = {funds}')
    total_value = funds + stock.last_price * stocks
    print(f'value = {total_value}')
    print(f'earnings = {round(total_value-start_with,2)}')
    returns = round((total_value/start_with-1)*100, 2)
    print(f'returns = {returns} %')

    return returns
