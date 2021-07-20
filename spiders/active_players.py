"""
    A spider to scrape all the active players for all 
    countries with available info in the database
"""
import scrapy
from ..items import TeamRosterInfoItem

class PlayersSpider(scrapy.Spider):
    name = 'players_spider'

    def start_requests(self):
        for i in range(1,10):
            url = f"https://hs-consumer-api.espncricinfo.com/v1/pages/player/search?mode=BOTH&filterTeamId={i}&filterFormatLevel=INTERNATIONAL"
        
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        if response.status == 200:
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