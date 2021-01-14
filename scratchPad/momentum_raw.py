from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging
from modules import instrumentData

logging.basicConfig(filename='myapp.log', level=logging.INFO)


class Momentum_Raw():
    def momentum_raw(self, symbol, exchange='LSE',
        roc_data_points = {'price_change_3_month': 3, 'price_change_6_month': 6, 'price_change_12_month': 12},
        sma_data_points = {'sma_10': 10, 'sma_30': 30, 'sma_100': 100},
        volume_data_points = {'volumeAverage_1': [0, 3], 'volumeAverage_2': [12, 15]},
        start = (datetime.today() + relativedelta(years=-1, months=-3)).date()):
        startStr = start.strftime('%Y-%m-%d')
        dfD = instrumentData.InstrumentData.getInstrumentTimeSeries('', symbol, exchange, startStr,
                                                                     end=datetime.today().date().strftime('%Y-%m-%d'))
        logging.debug(dfD)
        if dfD.empty:
            logging.debug('empty df')
            return dfD
        else:
            # Need a year and 3months' data and recent last updated price
            # get an array of dates and reindex dataframe

            dateArray = dfD.index.array
            dfD["new_index"] = range(0, len(dfD))
            hist = dfD.set_index('new_index')
            print(dfD)
            print(dateArray[len(dateArray)-1])
            print(start)
            print(start.strftime("%A"))
            earliestDate = dateArray[0]
            last_updated_date = dateArray[len(dateArray)-1]
            try:
                latestPrice = dfD.at[last_updated_date, "Close"]
                latestPrice = float(latestPrice)
                logging.debug("Latest Price " + str(latestPrice) + " on " + str(last_updated_date))
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
                output.update(calculateROC(last_updated_date, latestPrice, k, i, dfD))
            for k, i in sma_data_points.items():
                output.update(calculateSMA(last_updated_date, k, i, dfD, dateArray))
            for k, i in volume_data_points.items():
                output.update(calculateVolume(last_updated_date, k, i, dfD, dateArray))
            return output


def calculateROC(last_updated_date, latestPrice, key, period, dfD):
    finished = False
    n = 0
    while not finished:
        delta = relativedelta(months=-period, days=+n)
        date = last_updated_date + delta
        try:
            price = dfD.at[date, "Close"]
            price = float(price)
        except KeyError as e3:
            None
        else:
            finished = True
            roc = ((latestPrice - price) / price) * 100
            logging.debug("price " + str(price) + " on " + str(date))
            logging.debug(key + "month ROC is " + str(roc))
            return {key: roc}
        n += 1
        if n > 3:
            finished = True


def calculateSMA(last_updated_date, key, period, dfD, dateArray):
    sumPrices = 0
    for i in range(len(dateArray)-period-1, len(dateArray)-1):
        price = dfD.at[dateArray[i], "Close"]
        price = float(price)
        sumPrices += price
    sma = sumPrices/period
    return {key: sma}


def calculateVolume(last_updated_date, key, period, dfD, dateArray):
# find closest date to volume start and end dates

    rangeFrom = len(dateArray)-period[1]
    rangeTo = len(dateArray)-period[0]
    for i in range(rangeFrom, rangeTo):
        volToAdd = int(dfD.at[dateArray[i], "Volume"])
        print(dateArray[i].__str__() + str(volToAdd))
        volume += volToAdd
        n+=1
    avVolume = volume/(rangeTo - rangeFrom)
    return {key: avVolume}

if __name__ == '__main__':



    logging.info('starting main @ ' + datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
    symbol = 'NXT'
    exchange = 'LSE'
    momentumData = Momentum_Raw.momentum_raw('', symbol, exchange)
    logging.info(symbol)
    logging.info('3 month momentum is ' + str(momentumData['price_change_3_month']))
    logging.info('6 month momentum is ' + str(momentumData['price_change_6_month']))
    logging.info('12 month momentum is ' + str(momentumData['price_change_12_month']))
    logging.info('sma_10 is ' + str(momentumData['sma_10']))
    logging.info('sma_30 is ' + str(momentumData['sma_30']))
    logging.info('sma_100 is ' + str(momentumData['sma_100']))
    logging.info('volume_average_3m ' + str(momentumData['volume_average_3m']))
    logging.info('volume_average_historic is ' + str(momentumData['volume_average_historic']))


