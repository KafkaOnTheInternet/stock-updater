import requests
import sys
import os
import time
import pandas as pd

#url = 'https://query1.finance.yahoo.com/v7/finance/download/%5EDJI?period1=1607731200&period2=1608163200&interval=1d&events=history&includeAdjustedClose=false'
#r = requests.get(url, allow_redirects=True)


stock_names = []
deltas = {'1d': 1, '5d': 5}
num_seconds_1d = 24*60*60
base_url = 'https://query1.finance.yahoo.com/v7/finance/download/'
stock_folder = 'stocks/'
stock_file = 'stocks.txt'

def build_url(base_url, ticker, period1, period2):
    interval = '1d'
    filter_ = 'history'
    frequency= '1d'
    includeAdjustedClose='false'

    url = base_url + f'{ticker}?' + f'period1={period1}&' + f'period2={period2}&' + f'interval={interval}&' + 'events=history&' + 'includeAdjustedClose=false'

    return url


def download_stock(url, dirname='stocks/', fname='test'):
    r = requests.get(url, allow_redirects=True)
    fname += '.csv'
    open(dirname+fname, 'wb').write(r.content)

    df = pd.read_csv(dirname+fname, parse_dates=True).drop('Adj Close', axis=1)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Date'] = df['Date'].dt.strftime('%m/%d/%y')

    df.to_csv(dirname+fname, index=False)

    print(f'wrote file {fname}')

def get_stock_names(fname):
    names = None
    with open(fname) as f:
        names = [i.strip() for i in f.readlines()]
    print(names)
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
    
    for ticker in tickers:
        period2 = int(time.time())
        period1 = period2 - num_seconds_1d*deltas[delta]
        url = build_url(base_url, ticker, period1, period2)
        download_stock(url, fname=ticker)

'''
tickers = get_stock_names(stock_file)
delta = get_delta()
'''

loop()





 

