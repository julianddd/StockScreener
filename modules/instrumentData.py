import requests
import modules.data_source as ds
from datetime import datetime


def formatId(instrumentId, exchange):
    return {
        'LSE': lambda symbol: symbol + '.L'
    }[exchange](instrumentId)


class InstrumentData:

    def getInstrumentTechnical(self, instrumentId, exchange,
                               ti="MOM", interval="monthly", timePeriod=10, dataType="json"):
        # default case: use alphavantage.co
        symbol = formatId(instrumentId, exchange)
        url = "https://www.alphavantage.co/query?function=" + ti + "&symbol=" + symbol + "&interval=" + interval + \
              "&time_period=" + str(timePeriod) + "&series_type=close&datatype=" + dataType + "&apikey=2LZG74VZ3NDJBUOW"
        print(url)
        return requests.get(url).content

    def getInstrumentTimeSeries(self, instrumentId, exchange, timeSeries="TIME_SERIES_MONTHLY", outputSize="compact",
                                dataType="json"):
        symbol = formatId(instrumentId, exchange)
        url = "https://www.alphavantage.co/query?function=" + timeSeries + "&symbol=" + symbol + \
              "&outputsize=" + outputSize + "&datatype=" + dataType + "&apikey=2LZG74VZ3NDJBUOW"
        return requests.get(url).content


    def getInstrumentTimeSeries(self,instrumentId, exchange):
        symbol = formatId(instrumentId, exchange)
        return ds.DataSource.getInstrumentTimeSeries()


    def getInstrumentTimeSeries(self,instrumentId, exchange, start, end=datetime.today().date().strftime('%Y-%m-%d')):
        symbol = formatId(instrumentId, exchange)
        return ds.DataSource.getInstrumentTimeSeries(start, end)


if __name__ == '__main__':
#    iData = InstrumentData().getInstrumentTechnical('NXT', 'LSE')
    iData = InstrumentData().getInstrumentTimeSeries('NXT', 'LSE', '2019-10-05', '2021-01-05')
    print(iData)