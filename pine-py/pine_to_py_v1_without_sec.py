from tkinter.messagebox import NO
import pandas as pd
import shutil
import os




def get_me_direction(me__isUp_prev_and__isDown, me_isDown_prev_and__isUp):
    me_direction = []
    for i in range(len(me__isUp_prev_and__isDown)):
        if me__isUp_prev_and__isDown[i]:
            me_direction.append(-1)
        elif me_isDown_prev_and__isUp[i]:
            me_direction.append(1)
        else:
            try:
                me_direction.append(me_direction[-1])
            except:
                me_direction.append(1)
    return me_direction

def get_me_zigzag(me_isUp_prev_and__isDown_direction_prev, me_isDown_prev_and__isUp_and_direction_prev, me_highest2, me_lowest2):
    # _zigzag = _isUp[1] and _isDown and _direction[1] != -1 ? highest(2) : _isDown[1] and _isUp and _direction[1] != 1 ? lowest(2) : na
    me_zigzag = []
    for i in range(len(me_isUp_prev_and__isDown_direction_prev)):
        if (me_isUp_prev_and__isDown_direction_prev[i]):
            me_zigzag.append(me_highest2[i])
        elif (me_isDown_prev_and__isUp_and_direction_prev[i]):
            me_zigzag.append(me_lowest2[i])
        else:
            me_zigzag.append(None)
    return me_zigzag

def get_me_change_tf(time_tf):
    me_time_tf = []
    for i in range(len(time_tf)):
        if i == 0:
            me_time_tf.append(0)
        else:
            me_time_tf.append(time_tf[i] - time_tf[i-1])
    return me_time_tf

def get_me_sz(me_change_tf, sec):
    me_sz = [None if me_change_tf[i] == 0 else sec[i] for i in range(len(me_change_tf))]
    return me_sz

def valuewhen(me_sz, cntr):
    vals = [i for i in me_sz if((str(i) != 'nan') and (str(i) != 'None'))]
    prev = 0
    r=[]
    for i in me_sz:
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
    for i in range(len(a)):
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

original_dir = "C:/Users/HENOK/Downloads/BINANCE_BTCUSDTPERP, 30.csv"
tv_data_fn = "C:/Users/HENOK/Documents/Projects/TRDR/pine-py/output/BINANCE_BTCUSDTPERP, 30.csv"

try:
    os.remove(tv_data_fn)
    print('old file deleted')
except:
    print("Error while deleting file ", tv_data_fn)
shutil.move(original_dir, tv_data_fn)
df = pd.read_csv(tv_data_fn)
me_df = pd.DataFrame()



target01_trade_size = 1.00
target01_ew_rate = 0.236
target01_tp_rate = 0.618
target01_sl_rate = -0.236
target02_active = False
target02_trade_size = 1.00
target02_ew_rate = 0.236
target02_tp_rate = 1.618
target02_sl_rate = -0.236


close_price = list(df['close'])
open_price = list(df['open'])
high_price = list(df['high'])
low_price = list(df['low'])


me_isUp = [1 if(close_price[i] >= open_price[i]) else 0 for i in range(len(close_price))]
me_isDown  = [1 if(close_price[i] <= open_price[i]) else 0 for i in range(len(close_price))]
me_isUp_prev = [0] + me_isUp[:-1]
me__isUp_prev_and__isDown = [1 if (me_isUp_prev[i] and me_isDown[i]) else 0 for i in range(len(me_isUp_prev))]
me__isDown_prev = [0] + me_isDown[:-1]
me_isDown_prev_and__isUp = [1 if (me__isDown_prev[i] and me_isUp[i]) else 0 for i in range(len(me__isDown_prev))]
me_direction = get_me_direction(me__isUp_prev_and__isDown, me_isDown_prev_and__isUp)
me_direction_prev = [-1] + me_direction[:-1]
me_isUp_prev_and__isDown_direction_prev = [1 if(me_isUp_prev[i] and me_isDown[i] and me_direction_prev[i]) else 0 for i in range(len(me_isUp_prev))]
me_highest2 = [high_price[0] if i == 0 else max([high_price[i-1], high_price[i]]) for i in range(len(high_price))]
me_lowest2 = [low_price[0] if i == 0 else min([low_price[i-1], low_price[i]]) for i in range(len(low_price))]
me_isDown_prev_and__isUp_and_direction_prev = [1 if me_isDown_prev_and__isUp[i] and me_direction_prev[i] else 0 for i in range(len(me_isDown_prev_and__isUp))]
me_zigzag = get_me_zigzag(
    me_isUp_prev_and__isDown_direction_prev=me_isUp_prev_and__isDown_direction_prev,
    me_isDown_prev_and__isUp_and_direction_prev=me_isDown_prev_and__isUp_and_direction_prev,
    me_highest2=me_highest2,
    me_lowest2=me_lowest2,
)
me_change_tf = get_me_change_tf(list(df['time_tf']))
me_sz = get_me_sz(me_change_tf, list(df['sec']))

# Pattern Recognition:
x=valuewhen(me_sz, -4)
a=valuewhen(me_sz, -3)
b=valuewhen(me_sz, -2)
c=valuewhen(me_sz, -1)
d=valuewhen(me_sz, 0)

xab = get_xab(x,a,b)
xad = get_xad(x,a,d)
abc = get_abc(a,b,c)
bcd = get_bcd(b,c,d)


fib_range = fib_range(d, c)
_f_last_fib = f_last_fib(target01_ew_rate, fib_range, d, c)
_buy_patterns_00 = buy_patterns_00(
    isABCD(1, abc, bcd, d, c), isBat(1, xab, abc, bcd, xad, d, c), isAltBat(1, xab, abc, bcd, xad, d, c), isButterfly(1, xab, abc, bcd, xad, d, c),
    isGartley(1, xab, abc, bcd, xad, d, c), isCrab(1, xab, abc, bcd, xad, d, c),
    isShark(1, xab, abc, bcd, xad, d, c), is5o(1, xab, abc, bcd, xad, d, c), isWolf(1, xab, abc, bcd, xad, d, c),
    isHnS(1, xab, abc, bcd, xad, d, c), isConTria(1, xab, abc, bcd, xad, d, c), isExpTria(1, xab, abc, bcd, xad, d, c),
)
_buy_patterns_01 = buy_patterns_01(isAntiBat(1, xab, abc, bcd, xad, d, c), isAntiButterfly(1, xab, abc, bcd, xad, d, c), isAntiGartley(1, xab, abc, bcd, xad, d, c), isAntiCrab(1, xab, abc, bcd, xad, d, c), isAntiShark(1, xab, abc, bcd, xad, d, c))
_sel_patterns_00 = sel_patterns_00(isABCD(-1, abc, bcd, d, c), isBat(-1, xab, abc, bcd, xad, d, c), isAltBat(-1, xab, abc, bcd, xad, d, c), isButterfly(-1, xab, abc, bcd, xad, d, c), isGartley(-1, xab, abc, bcd, xad, d, c), isCrab(-1, xab, abc, bcd, xad, d, c), isShark(-1, xab, abc, bcd, xad, d, c), is5o(-1, xab, abc, bcd, xad, d, c), isWolf(-1, xab, abc, bcd, xad, d, c), isHnS(-1, xab, abc, bcd, xad, d, c), isConTria(-1, xab, abc, bcd, xad, d, c), isExpTria(-1, xab, abc, bcd, xad, d, c))
_sel_patterns_01 = sel_patterns_01(isAntiBat(-1, xab, abc, bcd, xad, d, c), isAntiButterfly(-1, xab, abc, bcd, xad, d, c), isAntiGartley(-1, xab, abc, bcd, xad, d, c), isAntiCrab(-1, xab, abc, bcd, xad, d, c), isAntiShark(-1, xab, abc, bcd, xad, d, c))
_target01_buy_entry = target01_buy_entry(_buy_patterns_00, _buy_patterns_01, close_price, f_last_fib(target01_ew_rate, fib_range, d, c))
_target01_buy_close = target01_buy_close(high_price, f_last_fib(target01_tp_rate, fib_range, d, c), low_price, f_last_fib(target01_sl_rate, fib_range, d, c))
_target01_sel_entry = target01_sel_entry(_sel_patterns_00, _sel_patterns_01, close_price, _f_last_fib)
_target01_sel_close = target01_sel_close(low_price, f_last_fib(target01_tp_rate, fib_range, d, c), high_price, f_last_fib(target01_sl_rate, fib_range, d, c))

me_df['time'] = list(df['time'])
me_df['open'] = open_price
me_df['close'] = close_price
me_df['high'] = high_price
# me_df['_isUp'] = list(df['_isUp'])
# me_df['me_isUp'] = me_isUp
# me_df['_isDown'] = list(df['_isDown'])
# me_df['me_isDown'] = me_isDown
# me_df['_isUp_prev'] = list(df['_isUp_prev'])
# me_df['me_isUp_prev'] = me_isUp_prev
# me_df['_isUp_prev_and__isDown'] = list(df['_isUp_prev_and__isDown'])
# me_df['me__isUp_prev_and__isDown'] = me__isUp_prev_and__isDown
# me_df['_isDown_prev'] = list(df['_isDown_prev'])
# me_df['me__isDown_prev'] = me__isDown_prev
# me_df['_isDown_prev_and__isUp'] = list(df['_isDown_prev_and__isUp'])
# me_df['me_isDown_prev_and__isUp'] = me_isDown_prev_and__isUp
# me_df['_direction'] = list(df['_direction'])
# me_df['me_direction'] = me_direction
# me_df['_direction_prev'] = list(df['_direction_prev'])
# me_df['me_direction_prev'] = me_direction_prev
# me_df['_isUp_prev_and__isDown_direction_prev'] = list(df['_isUp_prev_and__isDown_direction_prev'])
# me_df['me_isUp_prev_and__isDown_direction_prev'] = me_isUp_prev_and__isDown_direction_prev
# me_df['highest2'] = list(df['highest2'])
# me_df['me_highest2'] = me_highest2
# me_df['_isDown_prev_and__isUp_and_direction_prev'] = list(df['_isDown_prev_and__isUp_and_direction_prev'])
# me_df['me_isDown_prev_and__isUp_and_direction_prev'] = me_isDown_prev_and__isUp_and_direction_prev
# me_df['lowest2'] = list(df['lowest2'])
# me_df['me_lowest2'] = me_lowest2
# me_df['_zigzagg'] = list(df['_zigzagg'])
# me_df['me_zigzagg'] = me_zigzag
# me_df['time_tf'] = list(df['time_tf'])
# me_df['change_tf'] = list(df['change_tf'])
# me_df['me_change_tf'] = me_change_tf
# me_df['sec'] = list(df['sec'])
# me_df['sz'] = list(df['sz'])
# me_df['me_sz'] = me_sz
# me_df['x'] = list(df['x'])
# me_df['me_x'] = x
# me_df['a'] = list(df['a'])
# me_df['me_a'] = a
# me_df['b'] = list(df['b'])
# me_df['me_b'] = b
# me_df['c'] = list(df['c'])
# me_df['me_c'] = c
# me_df['d'] = list(df['d'])
# me_df['me_d'] = d
# me_df['bcd'] = list(df['bcd'])
# me_df['me_bcd'] = bcd
me_df['target01_sel_close'] = list(df['XS'])
me_df['me_target01_sel_close'] = _target01_sel_close

exp_fn = 'C:/Users/HENOK/Documents/Projects/TRDR/pine-py/output/me_df.csv'
me_df.to_csv(exp_fn, index=False)
os.system(f"start EXCEL.EXE {exp_fn}")
