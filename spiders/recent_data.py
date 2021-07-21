"""
    This spider processes JSON requests made by Cricinfo to load the latest scores
    and will store this data in a CSV.
"""

import scrapy
import json
import pandas as pd

class LiveScores(scrapy.Spider):
    name = "live_spider"

    start_urls = ['https://hs-consumer-api.espncricinfo.com/v1/pages/matches/current?latest=true']

    def pase(self, response):
        js = json.loads(response.body)

        js.to_json()
