from xmlrpc.client import boolean
from binance.client import Client
from datetime import datetime
import pandas as pd
import pickle
import time

t1=time.time()*1000
target01_trade_size = 1.00
target01_ew_rate = 0.236
target01_tp_rate = 0.618
target01_sl_rate = -0.236
target02_active = False
target02_trade_size = 1.00
target02_ew_rate = 0.236
target02_tp_rate = 1.618
target02_sl_rate = -0.236

def log_data(fn, val):
    with open(fn, "a") as myfile:
        myfile.write(val)

def update_var(fn, val):
    with open(fn, "w") as myfile:
        myfile.write(val)

def read_file(fn):
    with open(fn,'rb') as f:
        val = f.read()
    sp = val.decode('ascii')
    return sp

def get_my_direction(my__isUp_prev_and__isDown, my_isDown_prev_and__isUp):
    my_direction = []
    for i in range(len(my__isUp_prev_and__isDown)):
        if my__isUp_prev_and__isDown[i]:
            my_direction.append(-1)
        elif my_isDown_prev_and__isUp[i]:
            my_direction.append(1)
        else:
            try:
                my_direction.append(my_direction[-1])
            except:
                my_direction.append(1)
    return my_direction

def get_my_zigzag(my_isUp_prev_and__isDown_direction_prev, my_isDown_prev_and__isUp_and_direction_prev, my_highest2, my_lowest2):
    my_zigzag = []
    for i in range(len(my_isUp_prev_and__isDown_direction_prev)):
        if (my_isUp_prev_and__isDown_direction_prev[i]):
            my_zigzag.append(my_highest2[i])
        elif (my_isDown_prev_and__isUp_and_direction_prev[i]):
            my_zigzag.append(my_lowest2[i])
        else:
            my_zigzag.append(None)
    return my_zigzag

def get_my_change_tf(time_tf):
    my_time_tf = []
    for i in range(len(time_tf)):
        if i == 0:
            my_time_tf.append(0)
        else:
            diff = time_tf[i] - time_tf[i-1]
            if diff < 0:
                my_time_tf.append(0)
            else:
                my_time_tf.append(diff)
    return my_time_tf

def get_my_sz(my_change_tf, sec):
    my_sz = [None if my_change_tf[i] == 0 else sec[i] for i in range(len(my_change_tf))]
    return my_sz

def valuewhen(my_sz, cntr):
    vals = [i for i in my_sz if((str(i) != 'nan') and (str(i) != 'None'))]
    prev = 0
    r=[]
    for i in my_sz:
        if ((str(i) == 'nan') or (str(i) == 'None')):
            r.append(prev)
        else:
            if cntr < 0:
                r.append(prev)
                cntr += 1
            else:
                r.append(vals[cntr])
                prev = vals[cntr]
                cntr += 1
    return r

def get_xab(x,a,b):
    r=[]
    for i in range(len(a)):
        try:
            r.append(abs(b[i]-a[i])/abs(x[i]-a[i]))
        except:
            r.append(0)
    return r

def get_xad(x,a,d):
    r=[]
    for i in range(len(a)):
        try:
            r.append(abs(a[i]-d[i])/abs(x[i]-a[i]))
        except:
            r.append(0)
    return r

def get_abc(a,b,c):
    r=[]
    for i in range(len(a)):
        try:
            r.append(abs(b[i]-c[i])/abs(a[i]-b[i]))
        except:
            r.append(0)
    return r

def get_bcd(b,c,d):
    r=[]
    for i in range(len(b)):
        try:
            r.append(abs(c[i]-d[i])/abs(b[i]-c[i]))
        except:
            r.append(0)
    return r

def isBat(_mode, xab, abc, bcd, xad, d, c):
    r=[]
    for i in range(len(abc)):
        _xab = xab[i] >= 0.382 and xab[i] <= 0.5
        _abc = abc[i] >= 0.382 and abc[i] <= 0.886
        _bcd = bcd[i] >= 1.618 and bcd[i] <= 2.618
        _xad = xad[i] <= 0.618 and xad[i] <= 1.000
        r.append(0 if(_xab and _abc and _bcd and _xad and (d[i] < c[i] if(_mode == 1) else d[i] > c[i] )) == False else 1)
    return r

def isAntiBat(_mode, xab, abc, bcd, xad, d, c):
    r=[]
    for i in range(len(abc)):
        _xab = xab[i] >= 0.500 and xab[i] <= 0.886
        _abc = abc[i] >= 1.000 and abc[i] <= 2.618
        _bcd = bcd[i] >= 1.618 and bcd[i] <= 2.618
        _xad = xad[i] >= 0.886 and xad[i] <= 1.000
        r.append(0 if(_xab and _abc and _bcd and _xad and (d[i] < c[i] if(_mode == 1) else d[i] > c[i] )) == False else 1)
    return r

def isAltBat(_mode, xab, abc, bcd, xad, d, c):
    r=[]
    for i in range(len(abc)):
        _xab = xab[i] <= 0.382
        _abc = abc[i] >= 0.382 and abc[i] <= 0.886
        _bcd = bcd[i] >= 2.0 and bcd[i] <= 3.618
        _xad = xad[i] <= 1.13
        r.append(0 if(_xab and _abc and _bcd and _xad and (d[i] < c[i] if(_mode == 1) else d[i] > c[i] )) == False else 1)
    return r

def isButterfly(_mode, xab, abc, bcd, xad, d, c):
    r=[]
    for i in range(len(abc)):
        _xab = xab[i] <= 0.786
        _abc = abc[i] >= 0.382 and abc[i] <= 0.886
        _bcd = bcd[i] >= 1.618 and bcd[i] <= 2.618
        _xad = xad[i] >= 1.27 and xad[i] <= 1.618
        r.append(0 if(_xab and _abc and _bcd and _xad and (d[i] < c[i] if(_mode == 1) else d[i] > c[i] )) == False else 1)
    return r

def isAntiButterfly(_mode, xab, abc, bcd, xad, d, c):
    r=[]
    for i in range(len(abc)):
        _xab = xab[i] >= 0.236 and xab[i] <= 0.886
        _abc = abc[i] >= 1.130 and abc[i] <= 2.618
        _bcd = bcd[i] >= 1.000 and bcd[i] <= 1.382
        _xad = xad[i] >= 0.500 and xad[i] <= 0.886
        r.append(0 if(_xab and _abc and _bcd and _xad and (d[i] < c[i] if(_mode == 1) else d[i] > c[i] )) == False else 1)
    return r

def isABCD(_mode, abc, bcd, d, c):
    r=[]
    for i in range(len(abc)):
        _abc = abc[i] >= 0.382 and abc[i] <= 0.886
        _bcd = bcd[i] >= 1.13 and bcd[i] <= 2.618
        dlc = d[i] < c[i]
        dgc = d[i] > c[i]
        r.append(1 if _abc and _bcd and (dlc if _mode == 1 else dgc) else 0)
    return r

def isGartley(_mode, xab, abc, bcd, xad, d, c):
    r=[]
    for i in range(len(abc)):
        _xab = xab[i] >= 0.5 and xab[i] <= 0.618 
        _abc = abc[i] >= 0.382 and abc[i] <= 0.886
        _bcd = bcd[i] >= 1.13 and bcd[i] <= 2.618
        _xad = xad[i] >= 0.75 and xad[i] <= 0.875
        dlc = d[i] < c[i]
        dgc = d[i] > c[i]
        r.append(1 if _xab and _abc and _bcd and _xad and (dlc if _mode == 1 else dgc) else 0)
    return r

def isAntiGartley(_mode, xab, abc, bcd, xad, d, c):
    r=[]
    for i in range(len(abc)):
        _xab = xab[i] >= 0.500 and xab[i] <= 0.886
        _abc = abc[i] >= 1.000 and abc[i] <= 2.618
        _bcd = bcd[i] >= 1.500 and bcd[i] <= 5.000
        _xad = xad[i] >= 1.000 and xad[i] <= 5.000
        dlc = d[i] < c[i]
        dgc = d[i] > c[i]
        r.append(1 if _xab and _abc and _bcd and _xad and (dlc if _mode == 1 else dgc) else 0)
    return r

def isCrab(_mode, xab, abc, bcd, xad, d, c):
    r=[]
    for i in range(len(abc)):
        _xab = xab[i] >= 0.500 and xab[i] <= 0.875
        _abc = abc[i] >= 0.382 and abc[i] <= 0.886 
        _bcd = bcd[i] >= 2.000 and bcd[i] <= 5.000
        _xad = xad[i] >= 1.382 and xad[i] <= 5.000
        dlc = d[i] < c[i]
        dgc = d[i] > c[i]
        r.append(1 if _xab and _abc and _bcd and _xad and (dlc if _mode == 1 else dgc) else 0)
    return r

def isAntiCrab(_mode, xab, abc, bcd, xad, d, c):
    r=[]
    for i in range(len(abc)):
        _xab = xab[i] >= 0.250 and xab[i] <= 0.500
        _abc = abc[i] >= 1.130 and abc[i] <= 2.618
        _bcd = bcd[i] >= 1.618 and bcd[i] <= 2.618
        _xad = xad[i] >= 0.500 and xad[i] <= 0.750
        dlc = d[i] < c[i]
        dgc = d[i] > c[i]
        r.append(1 if _xab and _abc and _bcd and _xad and (dlc if _mode == 1 else dgc) else 0)
    return r

def isShark(_mode, xab, abc, bcd, xad, d, c):
    r=[]
    for i in range(len(abc)):
        _xab = xab[i] >= 0.500 and xab[i] <= 0.875
        _abc = abc[i] >= 1.130 and abc[i] <= 1.618
        _bcd = bcd[i] >= 1.270 and bcd[i] <= 2.240
        _xad = xad[i] >= 0.886 and xad[i] <= 1.130
        dlc = d[i] < c[i]
        dgc = d[i] > c[i]
        r.append(1 if _xab and _abc and _bcd and _xad and (dlc if _mode == 1 else dgc) else 0)
    return r

def isAntiShark(_mode, xab, abc, bcd, xad, d, c):
    r=[]
    for i in range(len(abc)):
        _xab = xab[i] >= 0.382 and xab[i] <= 0.875
        _abc = abc[i] >= 0.500 and abc[i] <= 1.000
        _bcd = bcd[i] >= 1.250 and bcd[i] <= 2.618
        _xad = xad[i] >= 0.500 and xad[i] <= 1.250
        dlc = d[i] < c[i]
        dgc = d[i] > c[i]
        r.append(1 if _xab and _abc and _bcd and _xad and (dlc if _mode == 1 else dgc) else 0)
    return r

def is5o(_mode, xab, abc, bcd, xad, d, c):
    r=[]
    for i in range(len(abc)):
        _xab = xab[i] >= 1.13 and xab[i] <= 1.618
        _abc = abc[i] >= 1.618 and abc[i] <= 2.24
        _bcd = bcd[i] >= 0.5 and bcd[i] <= 0.625
        _xad = xad[i] >= 0.0 and xad[i] <= 0.236
        dlc = d[i] < c[i]
        dgc = d[i] > c[i]
        r.append(1 if _xab and _abc and _bcd and _xad and (dlc if _mode == 1 else dgc) else 0)
    return r

def isWolf(_mode, xab, abc, bcd, xad, d, c):
    r=[]
    for i in range(len(abc)):
        _xab = xab[i] >= 1.27 and xab[i] <= 1.618
        _abc = abc[i] >= 0 and abc[i] <= 5
        _bcd = bcd[i] >= 1.27 and bcd[i] <= 1.618
        _xad = xad[i] >= 0.0 and xad[i] <= 5
        dlc = d[i] < c[i]
        dgc = d[i] > c[i]
        r.append(1 if _xab and _abc and _bcd and _xad and (dlc if _mode == 1 else dgc) else 0)
    return r

def isHnS(_mode, xab, abc, bcd, xad, d, c):
    r=[]
    for i in range(len(abc)):
        _xab = xab[i] >= 2.0 and xab[i] <= 10
        _abc = abc[i] >= 0.90 and abc[i] <= 1.1
        _bcd = bcd[i] >= 0.236 and bcd[i] <= 0.88
        _xad = xad[i] >= 0.90 and xad[i] <= 1.1
        dlc = d[i] < c[i]
        dgc = d[i] > c[i]
        r.append(1 if _xab and _abc and _bcd and _xad and (dlc if _mode == 1 else dgc) else 0)
    return r

def isConTria(_mode, xab, abc, bcd, xad, d, c):
    r=[]
    for i in range(len(abc)):
        _xab = xab[i] >= 0.382 and xab[i] <= 0.618
        _abc = abc[i] >= 0.382 and abc[i] <= 0.618
        _bcd = bcd[i] >= 0.382 and bcd[i] <= 0.618
        _xad = xad[i] >= 0.236 and xad[i] <= 0.764
        dlc = d[i] < c[i]
        dgc = d[i] > c[i]
        r.append(1 if _xab and _abc and _bcd and _xad and (dlc if _mode == 1 else dgc) else 0)
    return r

def isExpTria(_mode, xab, abc, bcd, xad, d, c):
    r=[]
    for i in range(len(abc)):
        _xab = xab[i] >= 1.236 and xab[i] <= 1.618
        _abc = abc[i] >= 1.000 and abc[i] <= 1.618
        _bcd = bcd[i] >= 1.236 and bcd[i] <= 2.000
        _xad = xad[i] >= 2.000 and xad[i] <= 2.236
        dlc = d[i] < c[i]
        dgc = d[i] > c[i]
        r.append(1 if _xab and _abc and _bcd and _xad and (dlc if _mode == 1 else dgc) else 0)
    return r

def fib_range(d, c):
    r=[]
    for i in range(len(d)):
        r.append(abs(d[i]-c[i]))
    return r


def f_last_fib(_rate, fib_range, d, c):
    r=[]
    for i in range(len(fib_range)):
        # d > c ? d-(fib_range*_rate):d+(fib_range*_rate)
        dgc = d[i] > c[i]
        r.append(d[i]-(fib_range[i]*_rate) if dgc else d[i]+(fib_range[i]*_rate))
    return r

def buy_patterns_00(_isABCD, _isBat, _isAltBat, _isButterfly, _isGartley, _isCrab, _isShark, _is5o, _isWolf, _isHnS, _isConTria, _isExpTria):
    r=[_isABCD[i] or _isBat[i] or _isAltBat[i] or _isButterfly[i] or _isGartley[i] or _isCrab[i] or _isShark[i] or _is5o[i] or _isWolf[i] or _isHnS[i] or _isConTria[i] or _isExpTria[i] for i in range(len(_isExpTria))]
    return r

def buy_patterns_01(_isAntiBat, _isAntiButterfly, _isAntiGartley, _isAntiCrab, _isAntiShark):
    r=[_isAntiBat[i] or _isAntiButterfly[i] or _isAntiGartley[i] or _isAntiCrab[i] or _isAntiShark[i] for i in range(len(_isAntiBat))]
    return r

def sel_patterns_00(_isABCD, _isBat, _isAltBat, _isButterfly, _isGartley, _isCrab, _isShark, _is5o, _isWolf, _isHnS, _isConTria, _isExpTria):
    r=[_isABCD[i] or _isBat[i] or _isAltBat[i] or _isButterfly[i] or _isGartley[i] or _isCrab[i] or _isShark[i] or _is5o[i] or _isWolf[i] or _isHnS[i] or _isConTria[i] or _isExpTria[i] for i in range(len(_isExpTria))]
    return r

def sel_patterns_01(_isAntiBat, _isAntiButterfly, _isAntiGartley, _isAntiCrab, _isAntiShark):
    r=[_isAntiBat[i] or _isAntiButterfly[i] or _isAntiGartley[i] or _isAntiCrab[i] or _isAntiShark[i] for i in range(len(_isAntiBat))]
    return r

def target01_buy_entry(_buy_patterns_00, _buy_patterns_01, _close, _f_last_fib):
    r=[]
    for i in range(len(_buy_patterns_00)):
        r.append(1 if (_buy_patterns_00[i] or _buy_patterns_01[i]) and _close[i] <= _f_last_fib[i] else 0)
    return r

def target01_buy_close(_high, _f_last_fib_target01_tp_rate, _low, _f_last_fib_target01_sl_rate):
    r = [1 if _high[i] >= _f_last_fib_target01_tp_rate[i] or _low[i] <= _f_last_fib_target01_sl_rate[i] else 0 for i in range(len(_f_last_fib_target01_tp_rate))]
    return r

def target01_sel_entry(_sel_patterns_00, _sel_patterns_01, _close, _f_last_fib):
    r=[1 if (_sel_patterns_00[i] or _sel_patterns_01[i]) and _close[i] >= _f_last_fib[i] else 0 for i in range(len(_f_last_fib))]
    return r

def target01_sel_close(_low, f_last_fib_target01_tp_rate, _high, _f_last_fib_target01_sl_rate):
    r=[1 if _low[i] <= f_last_fib_target01_tp_rate[i] or _high[i] >= _f_last_fib_target01_sl_rate[i] else 0 for i in range(len(_f_last_fib_target01_sl_rate))]
    return r

def sec60(my_zigzag60, time_tf):
    r=[]
    for i in range(len(time_tf)):
        if time_tf[i] == 0:
            if i > 0:
                r.append(my_zigzag60[i-1])
            else:
                r.append(my_zigzag60[i])
        else:
            r.append(my_zigzag60[i])
    return r


def read_pickle_file(fn):
    # with open(path_to_protocol5, "rb") as fh:
    with open(fn, 'rb') as handle:
        val = pickle.load(handle)
    print('read_pickle_file')
    return val

def format_time(lst):
    r = []
    for val in lst:
        sp1 = val.split('T')
        sp2 = sp1[1].split(':')
        sp3 = sp1[0].split('-')
        fd = f"{sp3[0]}-{sp3[1]}-{sp3[2]} {sp2[0]}:{sp2[1]}"
        r.append(fd)
    return r

def get_client():
    fn = '/home/ubuntu/key/binance-key.pickle'
    with open(fn, 'rb') as handle:
        k = pickle.load(handle)
    return Client(k['API_KEY'], k['API_SECRET'])

def get_historical_data(client, coin_pair, interval, start_ts, end_ts):
    # from_date = datetime.utcfromtimestamp(from_date_ts).strftime('%d-%m-%Y %H:%M:%S')
    # to_date = datetime.utcfromtimestamp(to_date_ts).strftime('%d-%m-%Y %H:%M:%S')
    # valid intervals - 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
    # 1h = KLINE_INTERVAL_1HOUR 
    # 30m = KLINE_INTERVAL_30MINUTE
    # returns OHLCV
    print('get_historical_data')
    return client.futures_historical_klines_generator(coin_pair, interval, start_ts, end_ts)

def prep60_data(tmf30_local_time, tmf60_local_time, data60):
    r = []
    append_val = 0.0
    for i in tmf30_local_time:
        if i in tmf60_local_time:
            idx = tmf60_local_time.index(i)
            append_val = data60[idx]
        r.append(append_val)
    print('prep60_data')
    return r


def process_8hr_data():
    client = get_client()
    four_hrs_ms = 14400000
    eight_hrs_ms = 28800000
    end_ts = int(time.time())*1000
    start_ts = end_ts - eight_hrs_ms
    
    d30 = list(get_historical_data(client, 'BTCUSDT', '30m', start_ts, end_ts))
    d60 = list(get_historical_data(client, 'BTCUSDT', '1h', start_ts, end_ts))

    my_df30 = pd.DataFrame()
    my_df60 = pd.DataFrame()
    comb_df = pd.DataFrame()

    utc_ts30 = [i[0] for i in d30]
    tmf30_local_time = [datetime.utcfromtimestamp((i[0]/1000)+four_hrs_ms/1000).strftime('%Y-%m-%dT%H:%M:00+04:00') for i in d30]
    open30 = [float(i[1]) for i in d30]
    high30 = [float(i[2]) for i in d30]
    low30 = [float(i[3]) for i in d30]
    close30 = [float(i[4]) for i in d30]

    my_df30['utc_ts30'] = utc_ts30
    my_df30['tmf30_local_time'] = tmf30_local_time
    my_df30['open30'] = open30
    my_df30['high30'] = high30
    my_df30['low30'] = low30
    my_df30['close30'] = close30

    utc_ts60 = [i[0] for i in d60]
    tmf60_local_time = [datetime.utcfromtimestamp((i[0]/1000)+four_hrs_ms/1000).strftime('%Y-%m-%dT%H:%M:00+04:00') for i in d60]
    open60 = [float(i[1]) for i in d60]
    high60 = [float(i[2]) for i in d60]
    low60 = [float(i[3]) for i in d60]
    close60 = [float(i[4]) for i in d60]

    nw_open60 = prep60_data(tmf30_local_time, tmf60_local_time, open60)
    nw_high60 = prep60_data(tmf30_local_time, tmf60_local_time, high60)
    nw_low60 = prep60_data(tmf30_local_time, tmf60_local_time, low60)
    nw_close60 = prep60_data(tmf30_local_time, tmf60_local_time, close60)
    new_tf60 = prep60_data(tmf30_local_time, tmf60_local_time, utc_ts60)

    comb_df['time'] = tmf30_local_time
    comb_df['open'] = open30
    comb_df['high'] = high30
    comb_df['low'] = low30
    comb_df['close'] = close30
    comb_df['close_60m'] = nw_close60
    comb_df['open_60m'] = nw_open60
    comb_df['high60'] = nw_high60
    comb_df['low60'] = nw_low60
    comb_df['time_tf'] = new_tf60

    
    # fn = 'C:/Users/HENOK/Downloads/BINANCE_BTCUSDTPERP, 30.csv'
    # print('BINANCE_BTCUSDTPERP, 30.csv exported!')
    # comb_df.to_csv(fn, index=False)
    print('-'*50)
    print('8Hrs Data')
    comb_df.tail()
    print('-'*50)
    return comb_df


def gen_positions():
    df = process_8hr_data()
    tm = list(df['time'])
    close_price = list(df['close'])
    open_price = list(df['open'])
    high_price = list(df['high'])
    low_price = list(df['low'])
    open_price60 = list(df['open_60m'])
    close_price60 = list(df['close_60m'])
    high_price60 = list(df['high60'])
    low_price60 = list(df['low60'])

    
    my_isUp = [1 if(close_price[i] >= open_price[i]) else 0 for i in range(len(close_price))]
    my_isUp60 = [1 if(close_price60[i] >= open_price60[i]) else 0 for i in range(len(close_price60))]
    my_isDown  = [1 if(close_price[i] <= open_price[i]) else 0 for i in range(len(close_price))]
    my_isDown60  = [1 if(close_price60[i] <= open_price60[i]) else 0 for i in range(len(close_price60))]
    my_isUp_prev = [0] + my_isUp[:-1]
    my_isUp_prev60 = [0] + my_isUp60[:-1]
    my__isUp_prev_and__isDown = [1 if (my_isUp_prev[i] and my_isDown[i]) else 0 for i in range(len(my_isUp_prev))]
    my__isUp_prev_and__isDown60 = [1 if (my_isUp_prev60[i] and my_isDown60[i]) else 0 for i in range(len(my_isUp_prev60))]
    my__isDown_prev = [0] + my_isDown[:-1]
    my__isDown_prev60 = [0] + my_isDown60[:-1]
    my_isDown_prev_and__isUp = [1 if (my__isDown_prev[i] and my_isUp[i]) else 0 for i in range(len(my__isDown_prev))]
    my_isDown_prev_and__isUp60 = [1 if (my__isDown_prev60[i] and my_isUp60[i]) else 0 for i in range(len(my__isDown_prev60))]
    my_direction = get_my_direction(my__isUp_prev_and__isDown, my_isDown_prev_and__isUp)
    my_direction60 = get_my_direction(my__isUp_prev_and__isDown60, my_isDown_prev_and__isUp60)
    my_direction_prev = [-1] + my_direction[:-1]
    my_direction_prev60 = [-1] + my_direction60[:-1]
    my_isUp_prev_and__isDown_direction_prev = [1 if(my_isUp_prev[i] and my_isDown[i] and my_direction_prev[i]) else 0 for i in range(len(my_isUp_prev))]
    my_isUp_prev_and__isDown_direction_prev60 = [1 if(my_isUp_prev60[i] and my_isDown60[i] and my_direction_prev60[i]) else 0 for i in range(len(my_isUp_prev60))]
    my_highest2 = [high_price[0] if i == 0 else max([high_price[i-1], high_price[i]]) for i in range(len(high_price))]
    my_highest260 = [high_price60[0] if i == 0 else max([high_price60[i-1], high_price60[i]]) for i in range(len(high_price60))]
    my_lowest2 = [low_price[0] if i == 0 else min([low_price[i-1], low_price[i]]) for i in range(len(low_price))]
    my_lowest260 = [low_price60[0] if i == 0 else min([low_price60[i-1], low_price60[i]]) for i in range(len(low_price60))]
    my_isDown_prev_and__isUp_and_direction_prev = [1 if my_isDown_prev_and__isUp[i] and my_direction_prev[i] else 0 for i in range(len(my_isDown_prev_and__isUp))]
    my_isDown_prev_and__isUp_and_direction_prev60 = [1 if my_isDown_prev_and__isUp60[i] and my_direction_prev60[i] else 0 for i in range(len(my_isDown_prev_and__isUp60))]

    my_zigzag = get_my_zigzag(
        my_isUp_prev_and__isDown_direction_prev=my_isUp_prev_and__isDown_direction_prev,
        my_isDown_prev_and__isUp_and_direction_prev=my_isDown_prev_and__isUp_and_direction_prev,
        my_highest2=my_highest2,
        my_lowest2=my_lowest2,
    )

    my_zigzag60 = get_my_zigzag(
        my_isUp_prev_and__isDown_direction_prev=my_isUp_prev_and__isDown_direction_prev60,
        my_isDown_prev_and__isUp_and_direction_prev=my_isDown_prev_and__isUp_and_direction_prev60,
        my_highest2=my_highest260,
        my_lowest2=my_lowest260,
    )

    time_tf = get_my_change_tf(list(df['time_tf']))
    my_sec = sec60(my_zigzag60, time_tf)

    my_change_tf = get_my_change_tf(time_tf)
    my_sz = get_my_sz(my_change_tf, my_sec)

    # Pattern Recognition:
    x=valuewhen(my_sz, -4)
    a=valuewhen(my_sz, -3)
    b=valuewhen(my_sz, -2)
    c=valuewhen(my_sz, -1)
    d=valuewhen(my_sz, 0)

    xab = get_xab(x,a,b)
    xad = get_xad(x,a,d)
    abc = get_abc(a,b,c)
    bcd = get_bcd(b,c,d)

    _fib_range = fib_range(d, c)
    _f_last_fib = f_last_fib(target01_ew_rate, _fib_range, d, c)
    _buy_patterns_00 = buy_patterns_00(
        isABCD(1, abc, bcd, d, c), isBat(1, xab, abc, bcd, xad, d, c), isAltBat(1, xab, abc, bcd, xad, d, c), isButterfly(1, xab, abc, bcd, xad, d, c),
        isGartley(1, xab, abc, bcd, xad, d, c), isCrab(1, xab, abc, bcd, xad, d, c),
        isShark(1, xab, abc, bcd, xad, d, c), is5o(1, xab, abc, bcd, xad, d, c), isWolf(1, xab, abc, bcd, xad, d, c),
        isHnS(1, xab, abc, bcd, xad, d, c), isConTria(1, xab, abc, bcd, xad, d, c), isExpTria(1, xab, abc, bcd, xad, d, c),
    )
    _buy_patterns_01 = buy_patterns_01(isAntiBat(1, xab, abc, bcd, xad, d, c), isAntiButterfly(1, xab, abc, bcd, xad, d, c), isAntiGartley(1, xab, abc, bcd, xad, d, c), isAntiCrab(1, xab, abc, bcd, xad, d, c), isAntiShark(1, xab, abc, bcd, xad, d, c))
    _sel_patterns_00 = sel_patterns_00(isABCD(-1, abc, bcd, d, c), isBat(-1, xab, abc, bcd, xad, d, c), isAltBat(-1, xab, abc, bcd, xad, d, c), isButterfly(-1, xab, abc, bcd, xad, d, c), isGartley(-1, xab, abc, bcd, xad, d, c), isCrab(-1, xab, abc, bcd, xad, d, c), isShark(-1, xab, abc, bcd, xad, d, c), is5o(-1, xab, abc, bcd, xad, d, c), isWolf(-1, xab, abc, bcd, xad, d, c), isHnS(-1, xab, abc, bcd, xad, d, c), isConTria(-1, xab, abc, bcd, xad, d, c), isExpTria(-1, xab, abc, bcd, xad, d, c))
    _sel_patterns_01 = sel_patterns_01(isAntiBat(-1, xab, abc, bcd, xad, d, c), isAntiButterfly(-1, xab, abc, bcd, xad, d, c), isAntiGartley(-1, xab, abc, bcd, xad, d, c), isAntiCrab(-1, xab, abc, bcd, xad, d, c), isAntiShark(-1, xab, abc, bcd, xad, d, c))
    my_target01_buy_entry = target01_buy_entry(_buy_patterns_00, _buy_patterns_01, close_price, f_last_fib(target01_ew_rate, _fib_range, d, c))
    my_target01_buy_close = target01_buy_close(high_price, f_last_fib(target01_tp_rate, _fib_range, d, c), low_price, f_last_fib(target01_sl_rate, _fib_range, d, c))
    my_target01_sel_entry = target01_sel_entry(_sel_patterns_00, _sel_patterns_01, close_price, _f_last_fib)
    my_target01_sel_close = target01_sel_close(low_price, f_last_fib(target01_tp_rate, _fib_range, d, c), high_price, f_last_fib(target01_sl_rate, _fib_range, d, c))

    my_df = pd.DataFrame()
    my_df['time'] = tm
    my_df['open'] = open_price
    my_df['EL'] = my_target01_buy_entry
    my_df['XL'] = my_target01_buy_close
    my_df['ES'] = my_target01_sel_entry
    my_df['XS'] = my_target01_sel_close
    prev_pos = {'el':my_target01_buy_entry[-2], 'xl': my_target01_buy_close[-2], 'es': my_target01_sel_entry[-2], 'xs': my_target01_sel_close[-2]}
    print('-'*50)
    print('Positions')
    print(my_df.tail())
    print('-'*50)
    ts = (time.time()+14400)
    tm = datetime.utcfromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S')
    pos_log = f"'{'-'*50}\n{tm}\n{str(my_df.tail())}\n'"
    log_data('pos-log.txt', pos_log)
    return my_df, prev_pos

def process_positions():
    df,prev_pos = gen_positions()
    # prev_pos = {'el': 0, 'es': 0, 'xl': 0, 'xs': 1}
    open_pos = read_file('vars/open_pos.txt')
    print('raw_open_pos: ',open_pos)
    pos_type = read_file('vars/pos_type.txt')
    if open_pos == 'False':
        if(prev_pos['el'] == 1):
            update_var('vars/open_pos.txt', 'True')
            update_var('vars/pos_type.txt', 'el')
            print('Entry Long')
            return 'el'

        if(prev_pos['es'] == 1):
            update_var('vars/open_pos.txt', 'True')
            update_var('vars/pos_type.txt', 'es')
            print('Entry Short')
            return 'es'

    if open_pos == 'True':
        if pos_type == 'el':
            if(prev_pos['xl'] == 1):
                update_var('vars/open_pos.txt', 'False')
                update_var('vars/pos_type.txt', 'xl')
                print('Exit Long')
                return 'xl'
        if pos_type == 'es':
            if(prev_pos['xs'] == 1):
                update_var('vars/open_pos.txt', 'False')
                update_var('vars/pos_type.txt', 'xs')
                print('Exit Short')
                return 'xs'

def get_signal():
    df,p = gen_positions()
    print(p)
    if p['el']:
        return 'el'
    if p['es']:
        return 'es'
    if p['xl']:
        return 'xl'
    if p['xs']:
        return 'xs'
