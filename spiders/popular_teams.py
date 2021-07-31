"""
    This spider processes JSON requests made by Cricinfo to access the popular 
    teams' (according to ESPNCricinfo) information and store it in our data files
    to use it for some more scraping. 
"""

import scrapy
import json
from ..items import PopularTeamsItem

class PopularTeams(scrapy.Spider):
    name = "teams_spider"

    start_urls = ['https://hs-consumer-api.espncricinfo.com/v1/pages/team']

    def parse(self, response):

        js = json.loads(response.body)
        teams = js['content']['popularTeams']

        intTeams = teams['internationalTeams']

        for team in intTeams:
            team_info = PopularTeams(
                team_id = team['objectId'],
                team_name = team['longName']
            )
            yield {'team':team_info.__dict__}