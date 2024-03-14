import sqlite3

def insert_values(values, table_name):
    connection = sqlite3.connect(database='data/automatic_stocks.db')
    values.to_sql(table_name, con=connection, index=False, if_exists='append')
    connection.close()
    return
