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
        season_id INT PRIMARY KEY,
        league_title TEXT,
        season INT
    );
""")

# Creating another table with all matches info for the leagues scraped
c.execute("""
    CREATE TABLE IF NOT EXISTS matches(
        league_id INT,
        match_id INT PRIMARY KEY,
        FOREIGN KEY (league_id)
            REFERENCES leagues(season_id)
    );
""")

