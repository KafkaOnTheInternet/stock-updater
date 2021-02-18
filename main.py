import requests
import sys
import os
import time
import pandas as pd

#url = 'https://query1.finance.yahoo.com/v7/finance/download/%5EDJI?period1=1607731200&period2=1608163200&interval=1d&events=history&includeAdjustedClose=false'
#r = requests.get(url, allow_redirects=True)


stock_names = []
deltas = {'1d': 1, '5d': 5, '1y': 365, '5y': 365*5, '10y': 365*10}
num_seconds_1d = 24*60*60
base_url = 'https://query1.finance.yahoo.com/v7/finance/download/'
stock_folder = './stocks/' + sys.argv[1] + '/'
stock_file = 'stocks_full.txt'
wrong_tickers = []



def build_url(base_url, ticker, period1, period2):
    interval = '1d'
    filter_ = 'history'
    frequency= '1d'
    includeAdjustedClose='false'

    url = base_url + f'{ticker}?' + f'period1={period1}&' + f'period2={period2}&' + f'interval={interval}&' + 'events=history&' + 'includeAdjustedClose=false'

    return url


def download_stock(url, dirname='./stocks/', fname='test'):
    r = requests.get(url, allow_redirects=True)
    fname_orig = fname
    fname += '.csv'
    open(dirname+fname, 'wb').write(r.content)
    
    try:
        df = pd.read_csv(dirname+fname, parse_dates=True)
        df.insert(0, 'Name', fname_orig)
        df['Date'] = pd.to_datetime(df['Date'])
        df['Date'] = df['Date'].dt.strftime('%m/%d/%y')
    except:
        print(f'{dirname+fname} doesnt exist, deleting')
        wrong_tickers.append(fname)
        os.remove(dirname+fname)
        return
    df = df.drop(['Adj Close'], axis=1)
    df.to_csv(dirname+fname, header=False, index=False)

    print(f'wrote file {fname}')

def get_stock_names(fname):
    names = None
    with open(fname) as f:
        names = [i.strip() for i in f.readlines()]
#    print(names)
    return names


def get_delta():
    global deltas
    delta = sys.argv[1]
    if delta not in deltas:
        print('Time given isnt valid, put proper param and rerun')
        exit()
    return delta
    

def loop():
    tickers = get_stock_names(stock_file)
    delta = get_delta()
    cnt = 1    
    for ticker in tickers:

        if cnt % 1000 == 0:
            print('Sleeping for 30s')
            time.sleep(30)
            print('Resuming')
        cnt += 1
        period2 = int(time.time())
        period1 = period2 - num_seconds_1d*deltas[delta]
        url = build_url(base_url, ticker, period1, period2)
        download_stock(url, dirname=stock_folder, fname=ticker)
    print(wrong_tickers)
'''
tickers = get_stock_names(stock_file)
delta = get_delta()
'''

loop()





 

