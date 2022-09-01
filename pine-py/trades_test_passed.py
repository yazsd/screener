import pandas as pd
import os


fn = 'C:/Users/HENOK/Documents/Projects/TRDR/pine-py/output/my_df.csv'
df = pd.read_csv(fn)


def format_time(lst):
    r = []
    for val in lst:
        sp1 = val.split('T')
        sp2 = sp1[1].split(':')
        sp3 = sp1[0].split('-')
        fd = f"{sp3[0]}-{sp3[1]}-{sp3[2]} {sp2[0]}:{sp2[1]}"
        r.append(fd)
    return r

raw_time = list(df['time'])
ft = format_time(raw_time)
open_price = list(df['open'])
el = list(df['EL'])
xl = list(df['XL'])
es = list(df['ES'])
xs = list(df['XS'])

max_tst = len(ft)
# max_tst = 2100
open_pos = False
pos_type = ''
entry_price = 0.0
closing_price = 0.0
pnl = 0.0
trade_cntr = 1

comp_trade = {}
trades = []

for i in range(max_tst-1):
    tm = ft[i+1]
    if open_pos == False:
        if(el[i] == 1.0):
            open_pos = True
            pos_type = 'el'
            entry_price = open_price[i+1]
            # print(f'idx: {i}\tTrade #{trade_cntr}\tDate: {tm}\tPos: {pos_type}\tPrice: {entry_price}')
            comp_trade['trade_num'] = trade_cntr
            comp_trade['type_e'] = pos_type
            comp_trade['entry_time'] = tm
            comp_trade['entry_price'] = entry_price
            continue
        
        if(es[i] == 1.0):
            open_pos = True
            pos_type = 'es'
            entry_price = open_price[i+1]
            # print(f'idx: {i}\tTrade #{trade_cntr}\tDate: {tm}\tPos: {pos_type}\tPrice: {entry_price}')
            comp_trade['trade_num'] = trade_cntr
            comp_trade['type_e'] = pos_type
            comp_trade['entry_time'] = tm
            comp_trade['entry_price'] = entry_price
            continue

    if open_pos:
        if pos_type == 'el':
            if(xl[i] == 1.0):
                open_pos = False
                pos_type = 'xl'
                closing_price = open_price[i+1]
                pnl = round((closing_price*100/entry_price)-100.0, 2)
                # print('-'*100)
                comp_trade['trade_num'] = trade_cntr
                comp_trade['type_x'] = pos_type
                comp_trade['exit_time'] = tm
                comp_trade['exit_price'] = closing_price
                comp_trade['pnl'] = pnl
                trades.append(comp_trade)
                comp_trade = {}
                # print(f'idx: {i}\tTrade #{trade_cntr}\tDate: {tm}\tPos: {pos_type}\tPrice: {closing_price}\tPnL: {pnl}')
                trade_cntr += 1
                continue
        if pos_type == 'es':
            if(xs[i] == 1.0):
                open_pos = False
                pos_type = 'xs'
                closing_price = open_price[i+1]
                pnl = round((entry_price*100/closing_price)-100.0, 2)
                # print('-'*100)
                comp_trade['trade_num'] = trade_cntr
                comp_trade['type_x'] = pos_type
                comp_trade['exit_time'] = tm
                comp_trade['exit_price'] = closing_price
                comp_trade['pnl'] = pnl
                trades.append(comp_trade)
                comp_trade = {}
                # print(f'idx: {i}\tTrade #{trade_cntr}\tDate: {tm}\tPos: {pos_type}\tPrice: {closing_price}\tPnL: {pnl}')
                trade_cntr += 1
                continue

trades_fn = 'C:/Users/HENOK/Documents/Projects/TRDR/pine-py/output/trades.csv'
my_df = pd.DataFrame(trades)
my_df.to_csv(trades_fn, index=False)
os.system(f"start EXCEL.EXE {trades_fn}")
