import sqlite3
from sqlite3 import Error
import time
from modules.momentumraw import MomentumRaw
from modules.symbol_exception import SymbolException as SE
from utilities import dbUtils

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def main():
    database = r"C:\sqlite\db\StockScreener.db"
    sql_select_rows = """ SELECT symbol, exchange_id 
                          FROM security 
                          WHERE symbol IN 
                          (SELECT symbol 
                          FROM security 
                          EXCEPT SELECT symbol 
                          FROM symbol_exception)
                          AND symbol NOT IN
                          (SELECT symbol 
                          FROM momentum_raw) 
                      ;"""
    sql_upsert_row = """ INSERT INTO momentum_raw (symbol, price_change_3_month, price_change_6_month, 
                         price_change_12_month, sma_10, sma_30, sma_100, created_time, last_updated_time) 
                         VALUES (?,?,?,?,?,?,?,?,?)
                         ON CONFLICT(symbol) DO UPDATE SET last_updated_time=excluded.last_updated_time,
                         price_change_3_month  = excluded.price_change_3_month,
                         price_change_6_month  = excluded.price_change_6_month,
                         price_change_12_month  = excluded.price_change_12_month,
                         sma_10 = excluded.sma_10,
                         sma_30 = excluded.sma_30,
                         sma_100 = excluded.sma_100
                     ;"""
    # create a database connection
    conn = create_connection(database)


    if conn is not None:
# select ids
        try:
            c = conn.cursor()


            c.execute(sql_select_rows)
            records = c.fetchall()
            print("Total rows are:  ", len(records))
            for row in records:
                symbol = row[0]
                print(symbol)
                time_waited = 0
                done = False
                while time_waited >= 120 or done is False:
                    momentumData = MomentumRaw.momentum_raw('', symbol)
                    print(momentumData)
#                    input("continue")
                    print(momentumData.keys())
                    if momentumData.keys().__contains__("Error Message"):
                        done = True
                        SE.setSymbolException('', symbol, 'alphavantage')
                    elif momentumData.keys().__contains__("Note"):
                        print("limit reached, waiting")
                        time.sleep(60)
                        time_waited += 60
                    else:
                        dbUtils.upsert_table(conn, sql_upsert_row,
                        (symbol, momentumData.get('price_change_3_month'),
                        momentumData.get('price_change_6_month'),
                        momentumData.get('price_change_12_month'),
                        momentumData.get('sma_10'),
                        momentumData.get('sma_30'),
                        momentumData.get('sma_100'),
                        int(time.time()),
                        int(time.time())))
                        done = True
        except Error as e:
            print(e)
        conn.commit()
        conn.close()
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':

    main()