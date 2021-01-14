import sqlite3
from sqlite3 import Error
import time
from modules import instrumentIDs, instrumentData

import json
from flask import jsonify


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


def upsert_table(conn, sql_upsert_row, symbol, exchange_id):

    timeStamp = int(time.time())
    try:
        c = conn.cursor()
        c.execute(sql_upsert_row, (symbol, 3, 6, 12, timeStamp, timeStamp))
    except Error as e:
        print(e)



def main():
    database = r"C:\sqlite\db\StockScreener.db"
    sql_select_rows = """ SELECT symbol, exchange_id FROM security WHERE symbol="NXT"
                      ;"""
    sql_upsert_row = """ INSERT INTO momentum_raw (symbol, price_change_3_month, price_change_6_month, 
                         price_change_12_month, created_time, last_updated_time) VALUES (?,?,?,?,?,?)
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
                exchange_id = row[1]
                data = instrumentData.InstrumentData.getInstrumentTechnical('', symbol, exchange_id, "ROC", "monthly", 3)

                jsonData = json.loads(data)
                print(jsonData)
                upsert_table(conn, sql_upsert_row, symbol, exchange_id)
        except Error as e:
            print(e)
        conn.commit()
        conn.close()
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':

    main()