import unittest
import modules.momentumraw as mr
import pandas as pd


def readDF(DFType='Ascending'):
    dfAscending = pd.read_csv('..\\..\\data\\ut_momentum_raw_calculate_volume.csv')
    dfAscending['Date'] = pd.to_datetime(dfAscending['Date'])
    if DFType == 'Ascending':
        return dfAscending
    else:
        dfDescending = dfAscending.sort_values(by=["Date"], ascending=False)
        dfDescending.reset_index(inplace=True, drop=True)
        return dfDescending


class TestMomentumRaw(unittest.TestCase):

    def test_calculateROC(self):
        key = 'testKey'  # key - any key
        period = 1  # number of months back
        dF = readDF(DFType='Descending')
        last_updated_date = dF.iloc[0, 0]
        latestPrice = dF.iloc[0, 4]
        output = mr.calculateROC(last_updated_date, latestPrice, key, period, dF)
        expected = str(8.15)
        actual = "{:.2f}".format(output['testKey'])
        self.assertEqual(expected, actual)

    def test_calculateSMA(self):
        key = 'testKey'  # key - any key
        period = 10  # number of periods for average
        dF = readDF(DFType='Descending')
        output = mr.calculateSMA(key, period, dF)
        self.assertEqual(6914.4, output['testKey'])

    def test_calculateVolume(self):
        key = 'testKey'  # key - any key
        period = [0, 1]  # period - 2 element array for months apart
        dF = readDF(DFType='Descending')
        last_updated_date = dF.iloc[0, 0]
        output = mr.calculateVolume(last_updated_date, key, period, dF)
        expected = str(371394.71)
        actual = "{:.2f}".format(output['testKey'])
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
