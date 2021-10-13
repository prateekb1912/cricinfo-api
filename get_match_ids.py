"""
    This script scrapes the stats records and returns the content IDs for all matches in a series/tournament.
"""

import requests
from bs4 import BeautifulSoup
import re

# We will start with scraping only the franchisee-based T20 leagues and build on it.

header = "https://stats.espncricinfo.com/"
addon = "ci/engine/records/index.html"

page = requests.get(header+addon)

soup = BeautifulSoup(page.content, 'html.parser')

# Finding the specific list with all T20 league titles and IDs 
leagues_list = soup.find_all('ul', attrs={'class': 'Record'})[11]
leagues_links = [{link.text:int(re.findall("[0-9]+",link['href'])[0])} for link in leagues_list.find_all('a')]

results_links = [header+f"ci/engine/records/team/match_results_season.html?id={list(id.values())[0]};type=trophy" for id in leagues_links]

res_page = requests.get(results_links[6])
soup = BeautifulSoup(res_page.content, 'html.parser')

recTable = soup.find('table', attrs={'class':'recordsTable'})
season_links = [link['href'] for link in recTable.find_all('a')]

season_pages = requests.get(header+season_links[0])
soup = BeautifulSoup(season_pages.content, 'html.parser')

matchTable = soup.find('table', attrs = {'class': 'engineTable'})
matchIDs = [int(re.findall("[0-9]+", link['href'])[0]) for link in matchTable.find_all('a', string = 'T20')]

print(matchIDs)