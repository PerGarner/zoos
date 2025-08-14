import sqlite3
import pandas as pd
   
def db_connection():
    conn = sqlite3.connect('todo.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = db_connection()
    cur = conn.cursor()
    cur.execute('''DROP TABLE IF EXISTS dyrizoo''') 
    cur.execute('''CREATE TABLE IF NOT EXISTS dyrizoo (zoo TEXT, dyr TEXT, PRIMARY KEY (zoo,dyr))''')

    conn.commit() 

    df_dyrizoo = pd.DataFrame()
    df_dyrizoo = pd.read_csv("dyrizoo.csv")
    for index, row in df_dyrizoo.iterrows():
        cur.execute("INSERT INTO dyrizoo (zoo, dyr) VALUES (?, ?)", (row['Zoo'].strip(), row['Dyr'].strip().title()) )
    
    conn.commit()
    conn.close()
