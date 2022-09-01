from flask import Flask, render_template, request, flash, redirect, jsonify, json, send_file
from binance.client import Client
from binance.enums import *
from time import time
import logging
import sys
import pickle as pickle
from datetime import datetime
import ast

# from pushbullet import Pushbullet



app = Flask(__name__)
app.secret_key = b'somelongrandomstring'

UTC_OFFSET = 14400000
TRADE_SYMBOL = 'BUSDUSDT'
TRADE_QUANTITY = 99.5
BUSD_TRADE_PERCENTAGE = 99.5
SELL_PERCENTAGE = 99.5

trade_percentage = BUSD_TRADE_PERCENTAGE/100.0
sell_trade_percentage = SELL_PERCENTAGE/100.0

leverage = 5
caps = [100.0]
position = 'N'
last_pos = ''

def read_db():
    with open('db.csv', 'r') as f:
        val = f.read()
    return val

def write_to_db(val):
    with open("db.csv", "a") as myfile:
        myfile.write(str(val)+'\n')

def read_logs():
    with open("trade.log") as file:
        data = file.read()
    return data

def get_client():
    fn = 'C:/Users/HENOK/Documents/Bkey/binance-key.pickle'
    with open(fn, 'rb') as handle:
        k = pickle.load(handle)
    return Client(k['API_KEY'], k['API_SECRET'])


# client = get_client()


def get_balance(coin):
    account = client.get_account()
    balances = account['balances']
    for balance in balances:
        if balance['asset'] == coin:
            return float(balance['free'])
    return None

def get_price(coin):
    coin = f'{coin}USDT'
    all_prices = client.get_all_tickers()
    for pair in all_prices:
        if pair['symbol'] == coin:
            return float(pair['price'])
    return None


@app.route('/webhook', methods=['POST']) 
def webhook():
    global position
    print(request.json['bs'])
    bs = request.json['bs']
    log = f'{bs}'
    # if ((bs == 'EL') and (position == 'N')):
    #     client.futures_change_leverage(symbol='BTCUSDT', leverage=leverage)
    #     to = client.futures_create_order(symbol='BTCUSDT', type='MARKET', side='BUY', quantity=0.008)
    #     position = 'B'
    #     print(to)
    #     log = f'Entry Long - {str(to)}'

    # if ((bs == 'XL') and (position == 'B')):
    #     client.futures_change_leverage(symbol='BTCUSDT', leverage=leverage)
    #     to = client.futures_create_order(symbol='BTCUSDT', type='MARKET', side='SELL', quantity=0.008)
    #     position = 'N'
    #     print(to)
    #     log = f'Exit Long - {str(to)}'

    # if ((bs == 'ES') and (position == 'N')):
    #     client.futures_change_leverage(symbol='BTCUSDT', leverage=leverage)
    #     to = client.futures_create_order(symbol='BTCUSDT', type='MARKET', side='SELL', quantity=0.008)
    #     position = 'S'
    #     print(to)
    #     log = f'Entry Short - {str(to)}'
    #     

    # if ((bs == 'XS') and (position == 'S')):
    #     client.futures_change_leverage(symbol='BTCUSDT', leverage=leverage)
    #     to = client.futures_create_order(symbol='BTCUSDT', type='MARKET', side='BUY', quantity=0.008)
    #     position = 'N'
    #     print(to)
    #     log = f'Exit Short - {str(to)}'
    
    response = jsonify({'d': bs})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/data') 
def data():
    global last_pos
    bs = request.args.get('bs', default = '', type = str)
    ts = request.args.get('ts', default = '', type = str)
    val = f'{ts},{bs}'
    if(last_pos != bs):
        write_to_db(val)
        last_pos = bs
    print(val)
    return str(val)
    # return render_template('data.html')

if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
