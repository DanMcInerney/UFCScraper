import scrapy
import pandas as pd

class UfcFighterScraper(scrapy.Spider):
    # MUST DELETE THE HEADERS ON NEW SCRAPE
    name = 'ufc_fighter_scraper'
    allowed_domains = ['ufcstats.com']
    fighter_df = pd.read_csv('C:\\Users\\danhm\\PycharmProjects\\UFCScraper\\UFCScraper\\individuals.csv')
    # custom_settings = {
    #     'DOWNLOAD_DELAY': .5
    # }

    def start_requests(self):
        base_url = 'http://ufcstats.com/statistics/fighters?char='
        alphabet = 'abcdefghijklmnopqrstuvwxyz'

        for char in alphabet:
            url = base_url + char + '&page=all'
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        fighter_links = response.css('td.b-statistics__table-col a::attr(href)').getall()
        for fighter_link in fighter_links:
            if fighter_link not in self.fighter_df['url'].values:
                yield scrapy.Request(fighter_link, callback=self.parse_fighter)

    def parse_fighter(self, response):
        fighter_data = {}
        fighter_data['name'] = response.css('span.b-content__title-highlight::text').get().strip()
        # Remove " from nickname to match fight scraper
        fighter_data['nickname'] = response.xpath('/html/body/section/div/p/text()').get().strip().replace('"', '')
        # If there is no nickname, then replace it with '--'
        if len(fighter_data['nickname']) == 0:
            fighter_data['nickname'] = '--'

        # Extract other fighter data such as date of birth, weight, reach, height, etc.
        fighter_data['url'] = response.url
        fighter_data['dob'] = response.xpath('//i[contains(translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "dob:")]/following-sibling::text()').get().strip()
        fighter_data['weight'] = response.xpath('//i[contains(translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "weight:")]/following-sibling::text()').get().strip()
        fighter_data['reach'] = response.xpath('//i[contains(translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "reach:")]/following-sibling::text()').get().strip()
        fighter_data['height'] = response.xpath('//i[contains(translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "height:")]/following-sibling::text()').get().strip()
        fighter_data['stance'] = response.xpath('//i[contains(translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "stance:")]/following-sibling::text()').get().strip()
        yield fighter_data