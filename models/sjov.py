from database import db_connection

queridict = {
    'Hvor mange zoos har dyret?': ('SELECT dyr, COUNT(zoo) AS number FROM dyrizoo GROUP BY dyr ORDER BY number DESC, dyr', ['Dyr', 'Antal Zoos']),
    'Hvor mange dyr har hver zoo?': ('SELECT zoo, COUNT(dyr) AS number FROM dyrizoo GROUP BY zoo ORDER BY number DESC', ['Zoo', 'Antal dyr']),
    'Hvor mange dyr har hver zoo, som andre zoos ikke har?': (
        'SELECT zoo, COUNT(dyr) as number FROM dyrizoo NATURAL JOIN (SELECT dyr FROM dyrizoo GROUP BY dyr HAVING COUNT(zoo)=1) GROUP BY zoo ORDER BY number DESC',
        ['Dyr', 'Antal Zoos'])
}

class Dyrizoo:
    def __init__(self, dyr, zoo):
        self.dyr = dyr
        self.zoo = zoo

class Query:
    def __init__(self, text):
        self.text = text

def get_querylist():
    result =[]
    for q in queridict.keys():
        result.append(Query(q))
    return result

def get_columns(question):
    return queridict[question][1]

def get_query(question):
    conn = db_connection()
    cur = conn.cursor()

    query = queridict[question][0]

    cur.execute(query)
    rows = cur.fetchall()
    conn.close()

    result = []
    for row in rows:
        result.append(Dyrizoo(row[0],row[1]))

    return result