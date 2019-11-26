import requests

URL = "https://www.alphavantage.co/query"


def get_stock_value(symbol):
    PARAMS = {'function': 'GLOBAL_QUOTE',
              'symbol': symbol,
              'apikey': 'DZ91XGSZEHIR84PX'}

    r = requests.get(url=URL, params=PARAMS)

    data = r.json()

    print(data)
    print(data['Global Quote']['01. symbol'])
    print(data['Global Quote']['05. price'])
    return data['Global Quote']['05. price']


if __name__ == '__main__':
    get_stock_value('MSFT')