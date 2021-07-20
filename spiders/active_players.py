"""
    A spider to scrape all the active players for all 
    countries with available info in the database
"""
import scrapy

class PlayersSpider(scrapy.Spider):
    name = 'players_spider'

    def start_requests(self):
        urls = []

        for i in range(100):
            urls.append(f"https://www.espncricinfo.com/ci/content/player/country.html?country={i}")
        
        for url in urls:
            yield scrapy.Request(url, callback=self.parse)
