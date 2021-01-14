import sqlite3
from sqlite3 import Error
import time


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


def upsert_table(conn, sql_upsert_row, symbol):

    timeStamp = int(time.time())
    print("timestamp " + str(timeStamp))
    try:
        c = conn.cursor()
        c.execute(sql_upsert_row, (symbol, timeStamp, timeStamp))
    except Error as e:
        print(e)



def main(symbol):
    database = r"C:\sqlite\db\StockScreener.db"

    sql_upsert_row = """ INSERT INTO exchange (symbol, created_time, last_updated_time) VALUES (?,?,?)
                         ON CONFLICT(symbol) DO UPDATE SET last_updated_time=excluded.last_updated_time   
                     ;"""
    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create exchange table
        upsert_table(conn, sql_upsert_row, symbol)
        conn.commit()
        conn.close()
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main('XLON')