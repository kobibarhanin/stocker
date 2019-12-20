import sys
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client['stocker']
stocks_coll = db['stocks']
settings_coll = db['settings']
transactions_coll = db['transactions']


def reset(stocks):

    stocks_coll.drop()
    transactions_coll.drop()
    settings_coll.drop()

    stocks_coll.insert_many(stocks)
    settings_coll.insert_one({'name': 'funds', 'total': 10000})
    settings_coll.insert_one({'name': 'value', 'total': 10000})


def status():

    print('==================================')
    print('Holdings status:')
    print('==================================')
    for stock in stocks_coll.find():
        print(f'{stock["symbol"]} = {stock["amount"]}')

    print('==================================')
    print('Assets status:')
    print('==================================')
    funds = settings_coll.find_one({'name': 'funds'})
    value = settings_coll.find_one({'name': 'funds'})
    print(f'Funds: {funds["total"]}')
    print(f'Value: {value["total"]}')

    print('==================================')
    print('Transactions:')
    print('==================================')
    transactions = list(transactions_coll.find())
    idx = -15
    if len(transactions) < 15:
        idx = 0 - len(transactions)
    for transaction in transactions[idx:]:
        print('transaction: ' + transaction['transaction'])
    print('==================================')


if __name__ == '__main__':

    stocks = [
        {'symbol': 'MSFT', 'amount': 0},
        {'symbol': 'PANW', 'amount': 0},
        {'symbol': 'AAPL', 'amount': 0},
        {'symbol': 'GOOGL', 'amount': 0},
        {'symbol': 'FB', 'amount': 0},
        {'symbol': 'NVDA', 'amount': 0},
        {'symbol': 'AMZN', 'amount': 0},
        {'symbol': 'NFLX', 'amount': 0},
        {'symbol': 'ZS', 'amount': 0}
    ]

    #stocks_coll.update({'symbol': 'GOOGL'}, {'$set': {'amount': 0}})
    #transact.remove({'time':{'$lte':"2019-12-19 10:00:13"}})
    # 2019-12-19 10:00:13

    cmd = sys.argv[1]
    if cmd == 'reset':
        reset(stocks)
    elif cmd == 'status':
        status()
    else:
        print('Unknown command')
