import scrapy
import numpy as np

class UfcScraper(scrapy.Spider):
    name = 'ufc_scraper'
    allowed_domains = ['ufcstats.com']
    start_urls = ['http://ufcstats.com/statistics/events/completed?page=all']
    #fight_df = pd.read_csv('C:\\Users\\danhm\\PycharmProjects\\UFCScraper\\competitions.csv')

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

        # Extract the fight weightclass, method, round, time, time format, referee, and details

        # Perf of the night, sub of the night, other stuff adds elements to the Xpath
        weight_class = ''
        elem = 0
        while weight_class == '':
            weight_class = response.xpath('/html/body/section/div/div/div[2]/div[1]/i/text()')[elem].get().strip()
            elem += 1

        result = response.xpath('/html/body/section/div/div/div[1]/div[1]/i/text()').get().strip()
        method = response.xpath(
            '//i[contains(text(), "Method:")]/following-sibling::i[@style="font-style: normal"]/text()').get().strip()
        round = response.xpath('//i[contains(text(), "Round:")]/following-sibling::text()').get().strip()
        time = response.xpath('//i[contains(text(), "Time:")]/following-sibling::text()').get().strip()
        time_format = response.xpath('//i[contains(text(), "Time format:")]/following-sibling::text()').get().strip()
        referee = response.xpath('//i[contains(text(), "Referee:")]/following-sibling::span/text()').get().strip()
        player1_url = response.xpath('/html/body/section/div/div/div[1]/div[1]/div/h3/a/@href').get().strip()
        player2_url = response.xpath('/html/body/section/div/div/div[1]/div[2]/div/h3/a/@href').get().strip()

        # This gets the details if the fight was a finish
        details = response.xpath('//i[contains(text(), "Details:")]/ancestor::p[1]/text()').getall()[1].strip()
        # If it wasn't a finish, then we get the judges names and scores
        if details == '':
            details_nodes = response.css('i:contains("Details:") ~ i.b-fight-details__text-item')
            details = " ".join(
                [text.strip() for node in details_nodes for text in node.css('::text').getall() if text.strip()])

        # Remove " marks from beginning and end of string to match individuals.csv nickname
        player1_nickname = response.xpath('/html/body/section/div/div/div[1]/div[1]/div/p/text()').get().strip().replace('"', '')
        player2_nickname = response.xpath('/html/body/section/div/div/div[1]/div[2]/div/p/text()').get().strip().replace('"', '')
        # Conditionally assign '--' only if player1_nickname or player2_nickname is empty so it doesn't get assigned as
        # NaN which messes with pd.merge
        if len(player1_nickname) == 0:
            player1_nickname = '--'
        if len(player2_nickname) == 0:
            player2_nickname = '--'

        # Flatten the details and add them to the fight data
        fight_data.update({
            'result': result,
            'player1': fighters[0],
            'player2': fighters[1],
            'player1_url': player1_url,
            'player2_url': player2_url,
            'weightclass': weight_class,
            'method': method,
            'round': round,
            'time': time,
            'time_format': time_format,
            'referee': referee,
            'details': details,
            'player1_nickname': player1_nickname,
            'player2_nickname': player2_nickname
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
        fight_data_1 = self.parse_section('/html/body/section/div/div/section[3]/table', response, round)
        # Significant strikes
        fight_data_2 = self.parse_section('/html/body/section/div/div/section[5]/table', response, round)

        # Merge the two dictionaries into the existing fight_data dictionary
        fight_data.update(fight_data_1)
        fight_data.update(fight_data_2)

        yield fight_data

    def parse_section(self, section_xpath, response, round):
        section = response.xpath(section_xpath)
        row_elements = section.xpath('.//tr[@class="b-fight-details__table-row"]')

        # Get column names from the first row
        column_names = row_elements[0].xpath('./th/text()').getall()
        column_names = [name.strip() for name in column_names if name.strip() != '']  # Strip white spaces
        column_names = column_names[1:]

        # There's a bug in the site where it labels "Td" as "Td %" in the round by round table labels
        if column_names.count("Td %") > 1:
            index_to_replace = column_names.index("Td %")  # finds the first occurrence
            column_names[index_to_replace] = "Td"

        fight_data = {}
        for i, row_element in enumerate(row_elements[1:]):  # Skip header row
            fighter_names = row_element.xpath('./td/p/a/text()').getall()
            data_columns = row_element.xpath('./td/p/text()').getall()[2:]  # Skipping fighter names
            data_columns = [data.strip() for data in data_columns if data.strip() != '']  # Strip white spaces

            # Flatten the data
            for j, fighter in enumerate(fighter_names):
                for k, stat in enumerate(data_columns[j::2]):
                    key = ('p1' if j == 0 else 'p2') + '_rd' + str(i + 1) + '_' + column_names[k]
                    key = key.replace('.', '').replace(' ','_')  # Remove periods and replace spaces with underscores
                    if '%' not in key:  # Skip keys with '%'
                        fight_data[key] = stat

        # Fill in empty round stats with NaN
        fight_data_up_to_rd5 = {}
        round_1_keys = [key for key in fight_data.keys() if '_rd1_' in key]
        for k in round_1_keys:
            for i in range(1, 6):
                key = k.replace('rd1', 'rd' + str(i))
                # Put the data in the fight_data_up_to_rd5 dictionary
                if key in fight_data.keys():
                    fight_data_up_to_rd5[key] = fight_data[key]
                # Add in NaNs for rounds that don't exist up to round 5
                else:
                    fight_data_up_to_rd5[key] = np.nan

        return fight_data_up_to_rd5

