"""
    The first spider in this project which will be used to scrape and store
    all the T20I match results
"""
import scrapy
import pandas as pd
from ..items import CricinfoCrawlerItem

class T20ISpider(scrapy.Spider):
    name = "t20i"

    def start_requests(self):
        urls = []

        # URLS for all T20I results from 2005 to 2020 
        for year in range(2005, 2021):
            urls.append(f"https://stats.espncricinfo.com/ci/engine/records/team/match_results.html?class=3;id=${str(year)};type=year")
        
        for url in urls:
            yield scrapy.Request(url, callback=self.parse)
    
    def parse(self, response):
        """
            The data is stored in a table with each result in a different row
        """

        items = CricinfoCrawlerItem()
        
        table = response.xpath("//table")[0]

        # Get header row for column names
        header = table.xpath("//th/text()").getall()

        data_rows = table.xpath("//tr[@class='data1']")

        # Now we will store all the data as a Pandas Dataframe
        # and save it into a csv

        for row in data_rows:
            data = row.xpath("td//text()").getall()

            t20Is = pd.DataFrame(data, columns=header)

            t20Is.to_csv("./results.csv", sep = ',')








