import sqlite3
from sqlite3 import Error


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


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    database = r"C:\sqlite\db\StockScreener.db"

    sql_create_exchange_table = """CREATE TABLE IF NOT EXISTS exchange (
                                    id integer PRIMARY KEY,
                                    symbol text NOT NULL UNIQUE,
                                    created_time integer NOT NULL,
                                    last_updated_time integer NOT NULL
                                );"""

    sql_create_security_table = """ CREATE TABLE IF NOT EXISTS security (
                                        id integer PRIMARY KEY,
                                        symbol text NOT NULL UNIQUE,
                                        exchange_id text NOT NULL,
                                        created_time integer NOT NULL,
                                        last_updated_time integer NOT NULL,
                                        FOREIGN KEY (exchange_id) REFERENCES exchange (symbol)
                                    ); """

    sql_create_momentum_raw_table = """ CREATE TABLE IF NOT EXISTS momentum_raw (
                                        id integer PRIMARY KEY,
                                        symbol text NOT NULL UNIQUE,
                                        price_change_3_month,
                                        price_change_6_month,
                                        price_change_12_month,
                                        sma_10,
                                        sma_30,
                                        sma_100,
                                        created_time integer NOT NULL,
                                        last_updated_time integer NOT NULL,
                                        FOREIGN KEY (symbol) REFERENCES security (symbol)
                                    ); """

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create exchange table
        create_table(conn, sql_create_exchange_table)

        # create security table
        create_table(conn, sql_create_security_table)

        # create momentum_raw table
        create_table(conn, sql_create_momentum_raw_table)
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()