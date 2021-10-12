"""
    This script scrapes the stats records and returns the content IDs for all matches in a series/tournament.
"""

import requests
from bs4 import BeautifulSoup

# We will start with scraping only the franchisee-based T20 leagues and build on it.

url = "https://stats.espncricinfo.com/ci/engine/records/index.html"

page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')

# Finding the specific list with all T20 league titles and URLs 
leagues_list = soup.find_all('ul', attrs={'class': 'Record'})[11]
leagues_links = [{link.text:link['href']} for link in leagues_list.find_all('a')]

[print(ll) for ll in leagues_links]
