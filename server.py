from flask import Flask, render_template, jsonify, request
import random
import string
from api import get_stock_value

app = Flask(__name__)


@app.route('/')
def stocks_view_landing():
    return render_template('stocks_view.html',
                           version=''.join(random.choices(string.ascii_uppercase + string.digits, k=10)))

@app.route('/stock')
def net_view_main():
    print('* Scanning network')
    stocks = [{
        'name': 'Microsoft',
        'symbol': 'MSFT',
        'value': get_stock_value('MSFT')
    }]
    print(f'* Deploying stocks: {stocks}')
    return jsonify(stocks)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
