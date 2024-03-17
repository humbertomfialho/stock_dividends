import sqlite3
import pandas as pd

def select_table(table_name):
    connection = sqlite3.connect(database='data/automatic_stocks.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM ' + table_name)
    data = pd.DataFrame(cursor.fetchall(), columns=[col[0] for col in cursor.description]) 
    connection.close()
    return data
