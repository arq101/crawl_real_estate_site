# -*- coding: utf-8 -*-
import re
from datetime import datetime

from crawl_webpage import Crawler


class CrawlRightMoveSite(Crawler):
    """ Class offers methods to crawl real estate website and retrieve:
    agent name,
    date property was added to site,
    for-sale or to-rent,
    & number of properties added for the specified date.
    """

    def __init__(self, url_addr):
        self.url_addr = url_addr

    def get_agent_name(self):
        """ Gets the name of the agent that uploaded the property to the site.
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

    def _determine_date_day_suffix(self, date_obj):
        if 4 <= date_obj.day <= 20 or 24 <= date_obj.day <= 30:
            return 'th'
        else:
            return ["st", "nd", "rd"][date_obj.day % 10 - 1]

    def get_date_properties_added(self):
        """ Gets the number of properties added to the site per date.
        """
        soup_obj = self._get_html_content()
        count_properties_added_per_date = {}

        all_date_tags = soup_obj.findAll('p', {'class': 'branchblurb'})
        for dt in all_date_tags:

            # check for pattern: on 30/04/2015
            if re.match(r'\w+ on \d{2}/\d{2}/\d{4}', dt.text):

                # captures the date in dd/mm/yyy
                date_added = re.match(r'\w+ on (\d{2}/\d{2}/\d{4})', dt.text).group(1)
                date_obj = datetime.strptime(date_added, "%d/%m/%Y")
                suffix = self._determine_date_day_suffix(date_obj)

                # convert the date obj back to a string, eg. 02nd Jun 2015
                date_added = date_obj.strftime("%d{} %b %Y".format(suffix))

            elif re.search(r'Reduced today', dt.text):
                todays_dt = datetime.now()
                suffix = self._determine_date_day_suffix(todays_dt)
                date_added = todays_dt.strftime('%d{} %m %Y'.format(suffix))
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
