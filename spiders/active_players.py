"""
    A spider to scrape all the active players for all 
    countries with available info in the database
"""
import scrapy

class PlayersSpider(scrapy.Spider):
    name = 'players_spider'

    def start_requests(self):
        url = "https://www.espncricinfo.com/ci/content/player/country.html?country=160"
        
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        if response.status == 200:
            container = response.css("div.player-index-container")

            # Checking if players info are available for the team
            players_grid = container.css("div.player-index-grid")

            if len(players_grid > 0):
               team = container.css("h2::text").get()
               team = team.replace(" Players", "")

               