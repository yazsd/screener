from pynput.keyboard import Key, Controller
import time
from os import listdir
from os.path import isfile, join
import os
import datetime
import requests

keyboard = Controller()
page_reloaded = False
data_downloaded = False

def reload_page():
    global page_reloaded
    print('page reloading...')
    keyboard.type('window.location.reload();')
    keyboard.press(Key.enter)


def download_csv():
    global data_downloaded
    print('Donloading CSV...')
    time.sleep(1)
    keyboard.type("document.getElementsByClassName('js-backtesting-download')[0].click()")
    keyboard.press(Key.enter)
    data_downloaded = True


def get_lettest_data_fn():
    time.sleep(2)
    downloads_path = 'C:\\Users\\HENOK\\Downloads\\'
    onlyfiles = [f for f in listdir(downloads_path) if isfile(join(downloads_path, f))]
    last_modified_ts = []
    kv = {}

    for i in onlyfiles:
        ts = os.path.getmtime(downloads_path+i)
        last_modified_ts.append(ts)
        kv[str(ts)] = i



    lattest_data = downloads_path + (kv[str(max(last_modified_ts))])
    return lattest_data


def get_trade_type():
    lattest_data_fn = get_lettest_data_fn()

    with open(lattest_data_fn) as file:
        data = file.read()

    last_trade = data.split('\n')[-1]
    last_trade_sp = last_trade.split(',')
    last_trade_sp2 = data.split('\n')[-2].split(',')
    last_trade_sp = data.split('\n')[-1].split(',')
    if(last_trade_sp[3] == ''):
        return last_trade_sp2[1]
    else:
        return last_trade_sp[1]



reload_min = [29, 59, 13]
download_min = [30,0, 14]

while 1:
    now = datetime.datetime.now()
    minute = now.minute
    sec = now.second
    

    if((minute in reload_min) and (sec < 1)):
        reload_page()
        print(minute, sec)
    if((minute in download_min) and (sec < 2)):
        download_csv()
        trade_type = get_trade_type()
        print(trade_type)
        print(minute, sec)
        if(trade_type == 'Entry Long'):
            d={"bs": "EL"}
        if(trade_type == 'Entry Short'):
            d={"bs": "ES"}
        if(trade_type == 'Exit Long'):
            d={"bs": "XL"}
        if(trade_type == 'Exit Short'):
            d={"bs": "XS"}
  
        # url = 'http://18.117.252.6:8000/webhook'
        # r = requests.post(url, json=d)
        # print('r', r)
        # print('status', r.status_code)

    time.sleep(1)


