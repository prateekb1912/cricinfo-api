"""
    The first spider in this project which will be used to scrape and store
    all the T20I match results
"""
import scrapy
from ..items import T20IResultsItem

class T20ISpider(scrapy.Spider):
    name = "t20i_spider"

    def start_requests(self):
        urls = []

        # URLS for all T20I results from 2005 to 2020 
        for year in range(2005, 2021):
            urls.append(f"https://stats.espncricinfo.com/ci/engine/records/team/match_results.html?class=3;id={year};type=year")
        
        for url in urls:
            yield scrapy.Request(url, callback=self.parse)
    
    def parse(self, response):

        items = T20IResultsItem()

        table = response.xpath("//table")[0]
        
        # The data is stored in a table with each result in a different row
        header = ['team1', 'team2', 'winner', 'margin', 'venue', 'match_date', 'match_no']

        data_rows = table.xpath("//tr[@class='data1']")

        for row in data_rows:
            data = row.xpath("td//text()").getall()

            items = dict(zip(header, data))

            yield items