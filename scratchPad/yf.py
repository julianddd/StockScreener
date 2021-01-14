import yfinance as yf
import pandas as pd

msft = yf.Ticker("MSFT")


# get historical market data
hist = msft.history(start="2019-10-01", end="2021-01-01")


# hist.to_csv(r'C:\\Users\\Julian\\Development\\StockScreener\\test\\data\\ut_momentum_raw_calculate_volume.csv',
#             date_format="%Y-%m-%dT%H:%M:%S")
#hist = msft.history(start="2020-12-01", end="2021-01-08")
print(msft.info['forwardEps'])
print(msft.info)
#hist.set_index('Date', inplace=True)
hist.index = pd.to_datetime(hist.index)
hist.reset_index(inplace=True)
#dateArray = hist.index.array
#hist["new_index"] = range(0, len(hist))
#hist = hist.set_index('new_index')
print(hist)
#price = hist['Close'].where(hist.loc['Date'] == datetime.strptime("2020-12-31", "%Y-%m-%dT%H:%M:%S"))
hist = hist.sort_values(by=["Date"], ascending=False)
hist.reset_index()
print('after reset')
print(hist)
total = hist.iloc[0:10, 5:6].sum()
print(total)
print(hist.index.sort_values(ascending=False))
#print(hist.index.array[len(hist.index.array)-1])
#for i in range(len(hist.index.array)-11, len(hist.index.array)-1):
#    print(hist.loc[hist.index.array[i]])
#    print(hist.loc[hist.index.array[i], "Close"])


