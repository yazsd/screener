import pandas as pd
import pandas_ta as ta


def crossover(x, y):
    return x < y
def crossunder(x, y):
    return x > y

def signal(val):
    r = []
    for x in val:
        if x < 0:
            r.append(0)
        elif x > 0:
            r.append(1)
        else:
            r.append(2)
    return r

def fSignal(val):
    r = signal(val)
    s = []
    for i,v in enumerate(r):
        if i > 1:
            if v == r[i-1]:
                s.append('hold')
            else:
                if v == 0:
                    s.append('short')
                if v == 1:
                    s.append('long')
                if v == 2:
                    s.append('hold')
        else:
            s.append('hold')
    return s

data_fn = 'data/BINANCE_BTCUSDT, 60.csv'
df = pd.read_csv(data_fn)

fastLength = 14
slowlength = 20
MACDLength = 13


MACD = ta.ema(df["close"], length=fastLength) - ta.ema(df["close"], length=slowlength)
aMACD = ta.ema(MACD, MACDLength)
delta = MACD - aMACD
sig = signal(delta)
fSignal = fSignal(delta)

df['mMACD'] = MACD
df['maMACD'] = aMACD
df['mdelta'] = delta
df['mSignal'] = sig
df['fSignal'] = fSignal

price = list(df['close'])
signal = list(df['fSignal'])
tm = list(df['time'])

t_prices = []
t_signals = []
t_tms = []
t_pnl = []
p_pnl = []

trades = []
cap = 100

for idx, val in enumerate(list(df['fSignal'])):
    if ((val == 'long') or (val == 'short')):
        t_tms.append(tm[idx])
        t_signals.append(val)
        t_prices.append(price[idx])

for idx,val in enumerate(t_signals):
    if val == 'short':
        bp = t_prices[idx-1]
        sp = t_prices[idx]
        pnl = round((sp*100/bp)-100, 2)
        t_pnl.append(pnl)
        cap = round(100*(1+pnl/100),2)
        trades.append({'buy_time': t_tms[idx-1], 'buy_price': bp, 'sell_time': t_tms[idx], 'sell_price': sp, 'pnl': pnl, 'cap': cap})
    else:
        t_pnl.append(0)
                

df2 = pd.DataFrame(trades)
# df2['time'] = t_tms
# df2['price'] = t_prices
# df2['signal'] = t_signals
# df2['pnl'] = t_pnl

df2.to_csv('1atrades.csv', index=False)

# fn = '1ame.csv'
# df.to_csv(fn)
# MACD = ema(close, fastLength) - ema(close, slowlength)

# aMACD = ema(MACD, MACDLength)
# delta = MACD - aMACD
# if (crossover(delta, 0)) :
#     print('long')

# if (crossunder(delta, 0)) :
#     print('short')

