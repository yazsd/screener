from time import time
import pickle as pickle
from datetime import datetime
from peewee import *
import pandas as pd
import datetime
import pandas_ta as ta
import numpy as np


def read_pickle_file(fn):
    with open(fn, 'rb') as handle:
        val = pickle.load(handle)
    return val

def write_pickle(fn, val):
    try:
        with open(fn, 'wb') as handle:
            pickle.dump(val, handle, protocol=pickle.HIGHEST_PROTOCOL)
            print(f'\n{fn} exported')
    except:
        print(f'\nCould not export {fn}')


def ema(data, window):
    alpha = 2 /(window + 1.0)
    alpha_rev = 1-alpha
    n = data.shape[0]

    pows = alpha_rev**(np.arange(n+1))

    scale_arr = 1/pows[:-1]
    offset = data[0]*pows[1:]
    pw0 = alpha*alpha_rev**(n-1)

    mult = data*pw0*scale_arr
    cumsums = mult.cumsum()
    out = offset + cumsums*scale_arr[::-1]
    return out

sd = 1577836800000
ed  = 1641081600000

fn = '1h-BTCUSDT-01012020-02012022.pickle'

header = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'u1', 'u2', 'u3', 'u4', 'u5', 'u6']
d = read_pickle_file(fn)
print(len(d))
# d = d[-1000:]


print('len', len(d))
# d.insert(0,header)


fastLength = 14
slowlength = 20
MACDLength = 13


"""
strategy("MACD Strategy", overlay=true)
fastLength = input(12)
slowlength = input(26)
MACDLength = input(9)
MACD = ta.ema(close, fastLength) - ta.ema(close, slowlength)
aMACD = ta.ema(MACD, MACDLength)
delta = MACD - aMACD
if (ta.crossover(delta, 0))
	strategy.entry("MacdLE", strategy.long, comment="MacdLE")
if (ta.crossunder(delta, 0))
	strategy.entry("MacdSE", strategy.short, comment="MacdSE")
"""



df = pd.DataFrame(d, columns=header)
cp = [float(i) for i in df['close']]
close_prices = np.asarray(cp, dtype=np.float32)

fast_ema = ema(close_prices,fastLength)
slow_ema = ema(close_prices,slowlength)
MACD = fast_ema - slow_ema
aMACD = ema(MACD, MACDLength)
delta = MACD - aMACD

sig = ['buy' if i > 0 else 'sell' for i in delta]

# signal = []
# last_sig = ''

# for i in sig:
#     signal.append('hold' if last_sig == i else i)
#     last_sig = i

# buy_idx = []
# sell_idx = []


# for idx,val in enumerate(signal):
#     if val == 'buy':
#         buy_idx.append(idx)
#     if val == 'sell':
#         sell_idx.append(idx)

# if sell_idx[0] < buy_idx[0]:
#     del sell_idx[0]



# first_buy_idx = signal.index('buy')
# dt = [datetime.datetime.utcfromtimestamp(i/1000).strftime('%Y-%m-%d %H:%M:%S') for i in df['timestamp']]
# price = [i for i in df['close']]
# df['date'] = dt
# df['price'] = price
# df['signal'] = signal


# pnls=[]
# for i in range(len(buy_idx)):
#     buy_time = dt[buy_idx[i]]
#     sell_time = dt[sell_idx[i]]
#     buy_price = float(price[buy_idx[i]])
#     sell_price = float(price[sell_idx[i]])
#     pnl = round((sell_price*100/buy_price)-100, 2)
#     pnls.append({'buy_time': buy_time, 'buy_price': buy_price, 'sell_time': sell_time, 'sell_price': sell_price, 'pnl': pnl})

# for i in header:
#     df = df.drop(i, 1)

# cap = 100
# trades = []
# for i in pnls:
#     pnl = i['pnl']
#     cap = cap*(1+(pnl/100))
#     trades.append(round(cap,2))

# print('Bal: ', round(cap, 2))
# pnl_df = pd.DataFrame(pnls)
# pnl_df['trades'] = trades

# fn = 'tst.csv'
# fn2 = 'pnl.csv'
# df.to_csv(fn)
# pnl_df.to_csv(fn2)
