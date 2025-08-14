from database import db_connection
from wikiget import *

animals = []
cur_animal = 0

class Dyr:
    def __init__(self, dyr):
        self.dyr = dyr

class Zoo:
    def __init__(self,zoo):
        self.zoo = zoo

def get_animallist():
    if animals == []:
        conn = db_connection()
        cur = conn.cursor()
        query = "SELECT DISTINCT dyr FROM dyrizoo ORDER BY dyr"
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()      
        for row in rows:
            animals.append(Dyr(row[0]))
    return animals

def get_zoos(dyr):
    conn = db_connection()
    cur = conn.cursor()

    query = "SELECT zoo FROM dyrizoo WHERE dyr = '"+dyr+"'"
    cur.execute(query)
    rows = cur.fetchall()
    conn.close()

    result = []
    for row in rows:
        result.append(Zoo(row[0]))

    return result

def get_info(dyr):
    scraper = WikipediaAnimalScraper(language='da')
    try:
        return scraper.get_article_summary(dyr)['extract']
    except:
        return 'Ikke fundet'

