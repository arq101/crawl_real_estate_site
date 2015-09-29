# -*- coding: utf-8 -*-
import re
from datetime import datetime

from crawl_webpage import Crawler


class CrawlRightMoveSite(Crawler):

    def __init__(self, url_addr):
        self.url_addr = url_addr

    def get_agent_name(self):
        """ Gets the names of the agent that uploaded the property to the site.
        """
        soup_obj = self._get_html_content()
        agent_name = re.search(r'from (\w+.*),', soup_obj.title.text).group(1)
        return agent_name

    def get_property_listing_type(self):
        """ Gets the type of property advertised on the site: for sale or to rent.
        """
        soup_obj = self._get_html_content()
        propert_type = re.match(r'Find property (\w+\s\w+)', soup_obj.title.text).group(1)
        return propert_type.title()

    def get_date_properties_added(self):
        """ Gets the number of properties added to the site per date.
        """
        soup_obj = self._get_html_content()
        count_properties_added_per_date = {}

        all_date_tags = soup_obj.findAll('p', {'class': 'branchblurb'})
        for dt in all_date_tags:
            if re.match(r'\w+ on \d{2}/\d{2}/\d{4}', dt.text):

                # captures the date in dd/mm/yyy
                date_added = re.match(r'\w+ on (\d{2}/\d{2}/\d{4})', dt.text).group(1)
                date_obj = datetime.strptime(date_added, "%d/%m/%Y")

                # determine the suffix for the day
                if 4 <= date_obj.day <= 20 or 24 <= date_obj.day <= 30:
                    suffix = 'th'
                else:
                    suffix = ["st", "nd", "rd"][date_obj.day % 10 - 1]

                date_added = datetime.strftime(date_obj, "%d{} %b %Y".format(suffix))

            elif re.search(r'Reduced today', dt.text):
                todays_dt = datetime.now()
                date_added = todays_dt.strftime('%m/%d/%Y')
            else:
                date_added = 'date unknown'

            if date_added in count_properties_added_per_date:
                count_properties_added_per_date[date_added] += 1
            else:
                count_properties_added_per_date[date_added] = 1
        return count_properties_added_per_date

    def prepare_results(self):
        agent = self.get_agent_name()
        property_type = self.get_property_listing_type()
        properties_added_per_date = self.get_date_properties_added()

        for date, count in properties_added_per_date.items():
            self.list_results.append(
                {
                    'agent': agent,
                    'date': date,
                    'type': property_type,
                    'properties_added': count
                }
            )
