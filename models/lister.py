from database import db_connection
import re

class Dyrizoo:
    def __init__(self, dyr, zoo):
        self.dyr = dyr
        self.zoo = zoo

class Zoo:
    def __init__(self, zoo):
        self.zoo = zoo

# drop down menu
def list_zoos():
    conn = db_connection()
    cur = conn.cursor()
    cur.execute('SELECT DISTINCT Zoo FROM dyrizoo ORDER BY Zoo')
    db_zoos = cur.fetchall()

    result = []
    for zoo in db_zoos:
        result.append(Zoo(zoo[0]))
    conn.close()
    
    return result

def list_animals(zoo=None, søgeord=""):
    conn = db_connection()
    cur = conn.cursor()

    query = (
        'SELECT dyr, zoo FROM dyrizoo'
    )

    if zoo:
        query += " WHERE Zoo = '" + zoo + "'"

    if søgeord:
        if 'WHERE' in query:
            query += " AND dyr LIKE '%" + søgeord + "%' COLLATE NOCASE" 
        else:
            query += " WHERE Dyr LIKE '%" + søgeord + "%' COLLATE NOCASE" 
    query += ' ORDER BY Dyr'
    cur.execute(query)
    rows = cur.fetchall()
    conn.close()

    result = []
    for row in rows:
        result.append(Dyrizoo(row[0],row[1]))

    return result
