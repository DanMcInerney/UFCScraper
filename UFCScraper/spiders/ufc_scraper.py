import scrapy
from scrapy_splash import SplashRequest

class UfcScraper(scrapy.Spider):
    name = 'ufc_scraper'
    allowed_domains = ['ufcstats.com']
    start_urls = ['http://ufcstats.com/statistics/events/completed?page=all']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        for event in response.css('td.b-statistics__table-col'):

            # Check if the event has the "next.png" image
            next_event_img = event.xpath('.//img[contains(@src, "/next.png")]')
            if next_event_img:
                # This is a future event, skip it
                continue

            event_link = event.css('i.b-statistics__table-content a::attr(href)').get()
            if event_link:
                yield scrapy.Request(event_link, callback=self.parse_event)

    def parse_event(self, response):
        # Extract the event date and location
        event_date = response.xpath('//i[contains(text(), "Date:")]/following-sibling::text()').get().strip()
        event_location = response.xpath('//i[contains(text(), "Location:")]/following-sibling::text()').get().strip()
        event_url = response.url

        for fight in response.css(
                'tr.b-fight-details__table-row.b-fight-details__table-row__hover.js-fight-details-click::attr(onclick)'):
            onclick = fight.get()
            fight_link = onclick.split("'")[1]  # Extract the URL from the JavaScript function call
            yield scrapy.Request(fight_link, callback=self.parse_fight,
                                 meta={'event_date': event_date, 'event_location': event_location, 'event_url': event_url})

    def parse_fight(self, response):

        # Check that fight data is available
        stats_not_available_section = response.xpath('/html/body/section/div/div/section')
        if stats_not_available_section:
            section_text = stats_not_available_section.get()
            if "not currently available" in section_text:
                return

        fight_data = {}

        # Extract the fighter names
        fighters = response.css('h3.b-fight-details__person-name a::text').getall()
        # Strip whitespace from the fighter names
        fighters = [fighter.strip() for fighter in fighters]

        # Extract the fight method, round, time, time format, referee, and details
        method = response.xpath(
            '//i[contains(text(), "Method:")]/following-sibling::i[@style="font-style: normal"]/text()').get().strip()
        round = response.xpath('//i[contains(text(), "Round:")]/following-sibling::text()').get().strip()
        time = response.xpath('//i[contains(text(), "Time:")]/following-sibling::text()').get().strip()
        time_format = response.xpath('//i[contains(text(), "Time format:")]/following-sibling::text()').get().strip()
        referee = response.xpath('//i[contains(text(), "Referee:")]/following-sibling::span/text()').get().strip()

        # Flatten the details and add them to the fight data
        fight_data.update({
            'fighter': fighters[0],
            'opponent': fighters[1],
            'method': method,
            'round': round,
            'time': time,
            'time_format': time_format,
            'referee': referee,
        })

        # Get the event date and location from the meta data
        event_date = response.meta.get('event_date')
        event_location = response.meta.get('event_location')
        event_url = response.meta.get('event_url')

        # Add the event date and location to the fight_data dictionary
        fight_data.update({
            'event_date': event_date,
            'event_location': event_location,
            'event_url': event_url
        })

        # Call the function for each section
        # Totals
        fight_data_1 = self.parse_section('/html/body/section/div/div/section[3]', response)
        # Significant strikes
        fight_data_2 = self.parse_section('/html/body/section/div/div/section[5]', response)

        # Merge the two dictionaries into the existing fight_data dictionary
        fight_data.update(fight_data_1)
        fight_data.update(fight_data_2)

        yield fight_data

    def parse_section(self, section_xpath, response):
        section = response.xpath(section_xpath)
        row_elements = section.xpath('.//tr[@class="b-fight-details__table-row"]')

        # Get column names from the first row
        column_names = row_elements[0].xpath('./th/text()').getall()
        column_names = [name.strip() for name in column_names if name.strip() != '']  # Strip white spaces
        column_names = column_names[1:]  # Skip 'Fighter' column

        fight_data = {}
        for i, row_element in enumerate(row_elements[1:]):  # Skip header row
            fighter_names = row_element.xpath('./td/p/a/text()').getall()
            data_columns = row_element.xpath('./td/p/text()').getall()[2:]  # Skipping fighter names
            data_columns = [data.strip() for data in data_columns if data.strip() != '']  # Strip white spaces

            # Flatten the data
            for j, fighter in enumerate(fighter_names):
                for k, stat in enumerate(data_columns[j::2]):
                    key = ('f' if j == 0 else 'o') + '_rd' + str(i + 1) + '_' + column_names[k]
                    key = key.replace('.', '').replace(' ',
                                                       '_')  # Remove periods and replace spaces with underscores
                    if '%' not in key:  # Skip keys with '%'
                        fight_data[key] = stat
        return fight_data

    # def parse_fighter(self, response):
    #     # Parse fighter info
    #     fighter_data = {}
    #     name = response.css('span.b-content__title-highlight::text').get().strip()
    #     fighter_data['url'] = response.url
    #
    #     # Extract other fighter data such as date of birth, weight, reach, height, etc.
    #     fighter_data['dob'] = response.xpath('//i[contains(text(), "DOB:")]/following-sibling::text()').get().strip()
    #     fighter_data['weight'] = response.xpath('//i[contains(text(), "Weight:")]/following-sibling::text()').get().strip()
    #     fighter_data['reach'] = response.xpath('//i[contains(text(), "Reach:")]/following-sibling::text()').get().strip()
    #     fighter_data['height'] = response.xpath('//i[contains(text(), "Height:")]/following-sibling::text()').get().strip()
    #     fighter_data['stance'] = response.xpath('//i[contains(text(), "Stance:")]/following-sibling::text()').get().strip()
    #
    #     self.fighter_data[name] = fighter_data