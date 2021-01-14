import time
from utilities import dbUtils
import csv


class SymbolException:
    def setSymbolException(self, symbol, datasource):
        timeStamp = int(time.time())
        sql_upsert_row = """ INSERT INTO symbol_exception (symbol, data_source, created_time, last_updated_time) VALUES 
                             (?,?,?,?)
                             ON CONFLICT(symbol, data_source) DO UPDATE SET last_updated_time=excluded.last_updated_time
                        ;"""
    # create a database connection
        conn = dbUtils.create_connection(dbUtils.database)
        values = (symbol, datasource, timeStamp, timeStamp)
        dbUtils.upsert_table(conn, sql_upsert_row, values)


    def getSymbolException(self, symbol):
        sql_select_statement = """ SELECT symbol, data_source FROM symbol_exception where symbol = ?
                      ;"""
        # create a database connection
        conn = dbUtils.create_connection(dbUtils.database)
        values = symbol
        dbUtils.select_data(conn, sql_select_statement, values)


if __name__ == '__main__':
    print('running main')

    with open('..\\scratchPad\\symbols_temp.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            SymbolException.setSymbolException('', row[0], 'alphavantage')
 #           input('next!')
