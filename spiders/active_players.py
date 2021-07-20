"""
    A spider to scrape all the active players for all 
    countries with available info in the database
"""
import scrapy
from scrapy.selector import Selector
from ..items import TeamRosterInfoItem
from scrapy_selenium import SeleniumRequest
from selenium import webdriver


class PlayersSpider(scrapy.Spider):
    name = 'players_spider'

    start_urls = ['https://www.espncricinfo.com/player/team/australia-2']

    def __init__(self):
        driver = webdriver.Chrome(executable_path='/home/patrick/Downloads/chromedriver')

        driver.get('https://www.espncricinfo.com/player/team/australia-2')

        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        self.html = driver.page_source

        driver.close()

    def parse(self, response):
        response = Selector(text = self.html)
        teamRoster = TeamRosterInfoItem()
        container = response.css("div.player-index-container")

        # Checking if players info are available for the team
        players_grid = container.css("div.player-index-grid")

        if len(players_grid) > 0:
            team = container.css("h2::text").get()
            team = team.replace(" Players", "") 

            players = players_grid.css("div.index-data")

            teamRoster['team'] = team
            teamRoster['team_size'] = len(players)
            yield teamRoster