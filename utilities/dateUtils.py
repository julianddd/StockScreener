import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta


def getBusinessDaysIndex(toDate=(datetime.today() + relativedelta(years=-1, days=-5)).date(), fromDate=datetime.today().date()):
    return pd.bdate_range(toDate, fromDate)


if __name__ == '__main__':
    dateIndex = getBusinessDaysIndex()
    print(dateIndex)
    print(dateIndex.get_loc('2020-12-23'))
