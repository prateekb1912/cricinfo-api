from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess

setting = get_project_settings()

teams_process = CrawlerProcess(setting)

file = teams_process.crawl("teams_spider")

print("FILEEEE =====?????",file)

teams_process.start()



class PlayersCrawler:
    def __init__(self, team_info = dict()):
        self.spider = 'players_spider'
        self.process = CrawlerProcess(setting)
            
        for info in team_info.items():
            print("Scraping players from ", info[1])
            
            self.process.crawl(self.spider, team_id = info[0], team_name = info[1])
        
        self.process.start()

PlayersCrawler({6: "India"})