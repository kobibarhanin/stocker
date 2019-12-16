from flask import Flask, render_template, jsonify, request
import random
import string
from api import get_stock_value
import threading


app = Flask(__name__)
stock_name = 'Microsoft'

@app.route('/')
def stocks_view_landing():
    return render_template('stocks_view.html',
                           version=''.join(random.choices(string.ascii_uppercase + string.digits, k=10)))

@app.route('/stock')
def net_view_main():
    print('* Scanning network')
    stocks = [{
        'name': stock_name,
        'symbol': 'MSFT',
        'value': get_stock_value('MSFT')
    }]
    print(f'* Deploying stocks: {stocks}')
    return jsonify(stocks)


def collect_stock_data(stock_name):
    print('test')
    # with open('test.data','a') as td:
    #     td.write(stock_name)


if __name__ == '__main__':
    threading.Thread(target=collect_stock_data, args=(stock_name,)).start()
    app.run(host='0.0.0.0')
