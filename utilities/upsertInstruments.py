import time
import datetime
from modules import instrumentIDs
from modules import instrumentData
from utilities import dbUtils, ioUtils
import yfinance as yf


def main(symbol, exchange_id):
    sql_upsert_row = """ INSERT INTO security (symbol, created_time, last_updated_time, exchange_id, 
                         type, created_time_hr, last_updated_time_hr) VALUES (?,?,?,?,?,?,?)
                         ON CONFLICT(symbol) DO UPDATE SET created_time=excluded.created_time,
                         last_updated_time=excluded.last_updated_time, 
                         type=excluded.type, 
                         created_time_hr=excluded.created_time_hr, 
                         last_updated_time_hr=excluded.last_updated_time_hr   
                     ;"""
    # create a database connection
    conn = dbUtils.create_connection()

    if conn is not None:
        epoch = int(time.time())
        time_hr = datetime.datetime.fromtimestamp(epoch).strftime('%Y-%m-%d %H:%M:%S')
        ticker = yf.Ticker(instrumentData.formatId(symbol, exchange_id))
        print(symbol)
        try:
            securityType = ticker.info['legalType']
        except KeyError as e:
            print(e)
        except ImportError as ie:
            print(ie)
        except IndexError as ie2:
            print(ie2)
        except Exception as eE:
            print(eE)
        else:
            dbUtils.upsert_table(conn, sql_upsert_row,
                                 (symbol, epoch, epoch, exchange_id, securityType, time_hr, time_hr))
            conn.commit()
            conn.close()
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
#    idList = instrumentIDs.InstrumentIds.getInstrumentIds('','LSE')
    idList = ioUtils.readCSV()
#    main('EOWR', 'LSE')
    for each in idList:
#    ioUtils.writeCSV(idList)
       main(each[0], 'LSE')