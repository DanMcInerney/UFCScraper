import scrapy
import pandas as pd
import random

class BfoScraper(scrapy.Spider):
    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 560,
        }
    }
    handle_httpstatus_list = [403]
    name = "bfo_scraper"
    allowed_domains = ['bestfightodds.com']

    # REMOVING so other scrapers work when masterML doesn't exist
    # df = pd.read_csv('C:\\Users\\danhm\\PycharmProjects\\mmaai\\masterML.csv')
    #
    # unique_players1 = df['player1'].unique().tolist()
    # unique_players2 = df['player2'].unique().tolist()
    # all_unique_players = list(set(unique_players1 + unique_players2))
    # test = all_unique_players[0:1]

    # Form the starting URLs
    #start_urls = [f'https://www.bestfightodds.com/search?query={f}' for f in all_unique_players]
    #start_urls = [f'https://www.bestfightodds.com/search?query={f}' for f in test]

    # User agents list
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
        # Add more user agents if needed
    ]

    def start_requests(self):
        for url in self.start_urls:
            user_agent = random.choice(self.USER_AGENTS)
            yield scrapy.Request(url, headers={'User-Agent': user_agent}, callback=self.parse)

    def parse(self, response):
        # Check if the response status is 403
        if response.status == 403:
            with open('forbidden_response.html', 'wb') as f:
                f.write(response.body)
            self.logger.warning('Got a 403 response from %s', response.url)
        else:
            # Handle other responses as you normally would
            pass
