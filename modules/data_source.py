import yfinance as yf


class DataSource:
    @staticmethod
    def getInstrumentTimeSeries(symbol, period='1y'):
        symbolTicker = yf.Ticker(symbol)
        return symbolTicker.history(period=period)

    @staticmethod
    def getInstrumentTimeSeries(symbol, start, end):
        symbolTicker = yf.Ticker(symbol)
        return symbolTicker.history(start=start, end=end)
