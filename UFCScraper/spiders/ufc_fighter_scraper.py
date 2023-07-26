import scrapy

class UfcFighterScraper(scrapy.Spider):
    name = 'ufc_fighter_scraper'
    allowed_domains = ['ufcstats.com']

    def start_requests(self):
        base_url = 'http://ufcstats.com/statistics/fighters?char='
        alphabet = 'abcdefghijklmnopqrstuvwxyz'

        for char in alphabet:
            url = base_url + char + '&page=all'
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        fighter_links = response.css('td.b-statistics__table-col a::attr(href)').getall()
        for fighter_link in fighter_links:
            yield scrapy.Request(fighter_link, callback=self.parse_fighter)

    def parse_fighter(self, response):
        fighter_data = {}
        fighter_data['name'] = response.css('span.b-content__title-highlight::text').get().strip()
        fighter_data['url'] = response.url

        # Extract other fighter data such as date of birth, weight, reach, height, etc.
        fighter_data['dob'] = response.xpath('//i[contains(translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "dob:")]/following-sibling::text()').get().strip()
        fighter_data['weight'] = response.xpath('//i[contains(translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "weight:")]/following-sibling::text()').get().strip()
        fighter_data['reach'] = response.xpath('//i[contains(translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "reach:")]/following-sibling::text()').get().strip()
        fighter_data['height'] = response.xpath('//i[contains(translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "height:")]/following-sibling::text()').get().strip()
        fighter_data['stance'] = response.xpath('//i[contains(translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "stance:")]/following-sibling::text()').get().strip()

        yield fighter_data