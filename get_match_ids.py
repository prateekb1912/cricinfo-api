"""
    This script scrapes the stats records and returns the content IDs for all matches in a series/tournament.
"""

import requests
from bs4 import BeautifulSoup
import re
from utils import *

# We will start with scraping only the franchisee-based T20 leagues and build on it.

header = "https://stats.espncricinfo.com/"

addon = "ci/engine/records/index.html"

page = requests.get(header+addon)
soup = BeautifulSoup(page.content, 'html.parser')

conn = create_connection('leagues.db')
c = conn.cursor()

# Creating a table with league detaisl like title, ID, number of seasons
c.execute("""
    CREATE TABLE IF NOT EXISTS leagues(
        id INT PRIMARY KEY,
        title TEXT,
        seasons INT
    );
""")

# Creating another table with all matches info for the leagues scraped
c.execute("""
    CREATE TABLE IF NOT EXISTS matches(
        league_id INT,
        match_id INT PRIMARY KEY,
        FOREIGN KEY (league_id)
            REFERENCES leagues(id)
    );
""")

# Finding the specific list with all T20 league titles and IDs 
leagues_list = soup.find_all('ul', attrs={'class': 'Record'})[11]
leagues_links = [{link.text:int(re.findall("[0-9]+",link['href'])[0])} for link in leagues_list.find_all('a')]

for ll in leagues_links:
    league_name = list(ll.keys())[0]
    if league_name == 'ICC Intercontinental Cup':
        continue
    league_id = list(ll.values())[0]
    
    results_link = header+f"ci/engine/records/team/match_results_season.html?id={league_id};type=trophy"
    
    res_page = requests.get(results_link)
    soup = BeautifulSoup(res_page.content, 'html.parser')
    
    recTable = soup.find('table', attrs={'class':'recordsTable'})
    
    season_links = [link['href'] for link in recTable.find_all('a')]

    num_seasons = len(season_links)

    for s in season_links:
        season_page = requests.get(header+s)
        soup = BeautifulSoup(season_page.content, 'html.parser')

        matchTable = soup.find('table', attrs = {'class': 'engineTable'})
        matchLinks = matchTable.find_all('a', string = 'T20')

        matchIDs = [int(re.findall("[0-9]+", link['href'])[0]) for link in matchLinks]

        for id in matchIDs:
            c.execute("""
                INSERT INTO matches VALUES (?,?)""", (league_id, id))

    
    c.execute("""
        INSERT INTO leagues VALUES (?,?,?)""", (league_id, league_name, num_seasons))
    
conn.commit()
