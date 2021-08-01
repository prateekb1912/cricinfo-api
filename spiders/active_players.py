"""
    A spider to scrape all the active players for all 
    countries with available info in the database
"""
import scrapy
import json
from ..items import PlayersItem

class PlayersSpider(scrapy.Spider):
    name = "players_spider"
    
    def __init__(self, team_id = 1):
        self.base_url = "https://hs-consumer-api.espncricinfo.com/v1/pages/player/search"
        "?mode=BOTH&records=10"
        "&filterFormatLevel=INTERNATIONAL&filterActive=true&page=1"

        self.curr_url = self.base_url + "&filterTeamId = %d"%team_id

        self.start_urls = [self.curr_url]

    def parse(self, response):
        details = json.loads(response.body)

        print(self.curr_url.split('&'))

        playersItem = PlayersItem() 

        if details['results']:
            for player in details['results']:
                playersItem['player_id'] = (player['objectId'])
                playersItem['full_name'] = (player['longName'])
                playersItem['gender'] = player['gender']
                playersItem['role'] = player['playingRole']

                yield playersItem
            yield scrapy.Request(self.curr_url + "&page=%d"%i, callback=self.parse)
