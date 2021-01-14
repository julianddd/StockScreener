import sqlite3
from sqlite3 import Error
database = r"C:\sqlite\db\StockScreener.db"


def create_connection(db_file=database):
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


def upsert_table(conn, sql_upsert_row, values):
    try:
        c = conn.cursor()
        c.execute(sql_upsert_row, values)
        conn.commit()
    except Error as e:
        print(e)


def select_data(conn, sql_select_statement, values):
    try:
        c = conn.cursor()
        c.execute(sql_select_statement, values)
        records = c.fetchall()
        conn.close()
        return records
    except Error as e:
        print(e)


if __name__ == '__main__':
    conn = create_connection(database)
    sql_select_statement = """SELECT symbol, data_source FROM symbol_exception where symbol = ?;"""
    values = ('AGGB',)
    print(select_data(conn, sql_select_statement, values))
