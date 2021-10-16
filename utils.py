from sqlite3 import Error
import sqlite3

# The headers used while accessing the ESPNCricinfo website for our data.
headers = {
  'authority': 'hs-consumer-api.espncricinfo.com',
  'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.115 Safari/537.36',
  'accept': '*/*',
  'sec-gpc': '1',
  'origin': 'https://www.espncricinfo.com',
  'sec-fetch-site': 'same-site',
  'sec-fetch-mode': 'cors',
  'sec-fetch-dest': 'empty',
  'referer': 'https://www.espncricinfo.com/',
  'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'
}

def create_connection(db_file):
    """ Create a database connection to the SQLite database
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

def get_league_id(league_title, season):
    """
        Return the league_id for a specific season of any league
        we want to get the details for.
    """

    conn = create_connection('leagues.db')
    cur = conn.cursor()

    cur.execute("""
        SELECT season_id FROM leagues
        WHERE league_title = ? AND season = ?""", (league_title, season))

    res = cur.fetchall()[0][0]

    return res
