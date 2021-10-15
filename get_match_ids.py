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

# Creating a table with league details 
# season_id - a unique ID for each season of the leagues
# league_title -  the name of the league which will have multiple seasons
# season - the season number of the league with the unique ID
c.execute("""
    CREATE TABLE IF NOT EXISTS leagues(
        season_id INT PRIMARY KEY,
        league_title TEXT,
        season INT
    );
""")

# Creating another table with all matches info for the leagues added to the DB
c.execute("""
    CREATE TABLE IF NOT EXISTS matches(
        league_id INT,
        match_id INT PRIMARY KEY,
        FOREIGN KEY (league_id)
            REFERENCES leagues(season_id)
    );
""")

# We will be extracting the ids for only the 5 major T20 leagues
# IPL, BBL, CPL, PSL, T20 Blast
rec_header = soup.find("ul", attrs={'id':'subnav_tier1'})
leagues = ['IPL', 'BBL', 'CPL', 'PSL', 'Blast']

for league in leagues:
    lg_div = rec_header.findAll('a', text=re.compile(f'{league}*'))[0].next_sibling.next_sibling

    season_list = lg_div.find_all('li', attrs={'class':'sub_nav_item'})[1:]

    season_links = [item.findChild('a') for item in season_list]

    season_years = [int(re.findall("[0-9]+", link['name'])[0]) for link in season_links]
    season_ids = [int(re.findall("[0-9]+", link['href'])[0]) for link in season_links]

    print(f"{league} = {len(season_ids)}")


