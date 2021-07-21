"""
    A spider to scrape all the active players for all 
    countries with available info in the database
"""
import scrapy
import time
from scrapy.selector import Selector
from ..items import TeamRosterInfoItem
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class PlayersSpider(scrapy.Spider):
    name = 'players_spider'

    start_urls = ["https://www.espncricinfo.com/player/team/australia-"+str(id)
                  for id in range(4)]

    def __init__(self):
        self.driver = webdriver.Chrome(
            executable_path='/home/patrick/Downloads/chromedriver')

        # self.driver.implicitly_wait(10)
        self.wait = WebDriverWait(self.driver, 10)


    def parse(self, response):

        self.logger.debug(response.url)
        self.driver.get(response.url)
        
        # time.sleep(10)

        #self.wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.solid-loader")))

        self.html = self.driver.page_source

        response = Selector(text=self.html)
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
        self.driver.close()
