import aiohttp
import asyncio
import re

from bs4 import BeautifulSoup

class ScorecardScraper(object):
    def __init__(self, tournament_name, seasons):
        self.all_ids = []
        self.urls = [f'https://en.wikipedia.org/wiki/{season}_{tournament_name}' for season in seasons]

        asyncio.run(self.main())

    async def fetch(self, session, url):
        async with session.get(url) as resp:
            try:
                assert resp.status_code == 200
                
                body = resp.text()
                soup = BeautifulSoup(body, 'html.parser')

                scorecard_links = soup.find_all('a', string=re.compile('Scorecard*'))

                for link in scorecard_links:
                    match_id = int(link['href'].split('/')[-1].split('.html')[0], base=10)
                    self.all_ids.append(match_id)

            except Exception:
                pass

    async def main(self):
        tasks = []

        async with aiohttp.ClientSession() as session:
            for url in self.urls:
                tasks.append(asyncio.ensure_future(self.fetch(session, url)))
            
            await asyncio.gather(*tasks)


