from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging
from modules import instrumentData

logging.basicConfig(filename='myapp.log', level=logging.INFO)
global CLOSE, VOLUME, DATE, DIVIDENDS
DATE = 0
CLOSE = 4
VOLUME = 5
DIVIDENDS = 6


class MomentumRaw:
    def momentum_raw(self, symbol, exchange='LSE',
                     roc_data_points={'price_change_3_month': 3, 'price_change_6_month': 6,
                                      'price_change_12_month': 12},
                     sma_data_points={'sma_10': 10, 'sma_30': 30, 'sma_100': 100},
                     volume_data_points={'volume_average_1': [0, 3], 'volume_average_2': [12, 15]},
                     start=(datetime.today() + relativedelta(years=-1, months=-3)).date()):
        startStr = start.strftime('%Y-%m-%d')
        dfD = instrumentData.InstrumentData.getInstrumentTimeSeries('', symbol, exchange, startStr,
                                                                    end=datetime.today().date().strftime('%Y-%m-%d'))
        logging.debug(dfD)
        print(dfD)
        if dfD.empty:
            logging.debug('empty df')
            return dfD
        else:
            # Need a year and 3months' data and recent last updated price
            # get an array of dates and reindex dataframe
            dfDescending = dfD.sort_values(by=["Date"], ascending=False)
            dfD.reset_index(inplace=True)
            dfDescending.reset_index(inplace=True)
            print(dfD)
            print(dfDescending)
            lastPos = len(dfD) - 1
            earliestDate = dfD.iloc[0, DATE]
            last_updated_date = dfD.iloc[lastPos, DATE]
            try:
                latestPrice = dfD.iloc[lastPos, CLOSE]
                latestPrice = float(latestPrice)
            except TypeError as te:
                return {'Error Message': 'price check something is wrong' + str(te)}

            try:
                if last_updated_date < datetime.today().date() + relativedelta(days=-4):
                    return {'Error Message': 'date check something is wrong'}
            except KeyError as te:
                return {'Error Message': 'date check something is wrong' + str(te)}
            try:
                if earliestDate > start + relativedelta(days=4):
                    return {'Error Message': 'date check something is wrong'}
            except KeyError as te:
                return {'Error Message': 'date check something is wrong' + str(te)}
            output = {}
            for k, i in roc_data_points.items():
                output.update(calculateROC(last_updated_date, latestPrice, k, i, dfDescending))
            for k, i in sma_data_points.items():
                output.update(calculateSMA(k, i, dfDescending))
            for k, i in volume_data_points.items():
                output.update(calculateVolume(last_updated_date, k, i, dfDescending))
            return output


def calculateROC(last_updated_date, latestPrice, key, period, dfDescending):
    dateLoc = findNearestDate(last_updated_date, period, dfDescending)
    price = dfDescending.iloc[dateLoc, CLOSE]
    price = float(price)
    roc = ((latestPrice - price) / price) * 100
    return {key: roc}


def calculateSMA(key, period, dfDescending):
    sma = dfDescending.iloc[0:period, CLOSE:VOLUME].mean()
    return {key: sma['Close']}


def calculateVolume(last_updated_date, key, period, dfDescending):
    fromPosition = findNearestDate(last_updated_date, period[0], dfDescending)
    toPosition = findNearestDate(last_updated_date, period[1], dfDescending)
    averageVolume = dfDescending.iloc[fromPosition:toPosition, VOLUME:DIVIDENDS].mean()
    return {key: averageVolume["Volume"]}


def findNearestDate(date, period, localDF):
    finished = False
    n = 0
    while not finished:
        delta = relativedelta(months=-period, days=+n)
        searchDate = date + delta
        try:
            dateLoc = localDF[localDF['Date'] == searchDate].index.item()
            print(type(dateLoc))
        except ValueError as e3:
            None
        else:
            return dateLoc
        n += 1
        if n > 3:
            finished = True


if __name__ == '__main__':
    logging.info('starting main @ ' + datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
    symbol = 'NXT'
    exchange = 'LSE'
    momentumData = MomentumRaw.momentum_raw('', symbol, exchange)
    logging.info(symbol)
    logging.info('3 month momentum is ' + str(momentumData['price_change_3_month']))
    logging.info('6 month momentum is ' + str(momentumData['price_change_6_month']))
    logging.info('12 month momentum is ' + str(momentumData['price_change_12_month']))
    logging.info('sma_10 is ' + str(momentumData['sma_10']))
    logging.info('sma_30 is ' + str(momentumData['sma_30']))
    logging.info('sma_100 is ' + str(momentumData['sma_100']))
    logging.info('volume_average_1 ' + str(momentumData['volume_average_1']))
    logging.info('volume_average_2 is ' + str(momentumData['volume_average_2']))
