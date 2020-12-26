import pandas as pd

df = pd.read_csv('stocks_full.csv', header=None)

with open('stocks_full.txt', 'w') as f:
    tickers = df[0]
    for ticker in tickers:
        f.write(ticker + '\n')



