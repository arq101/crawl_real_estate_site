# -*- coding: utf-8 -*-

import re

from crawl_webpage import Crawler
import exceptions


class CrawlZooplaSite(Crawler):
    """ Class offers methods to crawl real estate website and display:
    agent name,
    date property was added to site,
    for-sale or to-rent,
    & number of properties added for the specified date.
    """

    def __init__(self, url_addr):
        self.url_addr = url_addr

    def get_agent_name(self):
        """ Gets the names of the agent that uploaded the property to the site.
        """
        soup_obj = self._get_html_content()

        agent_details = soup_obj.title.text
        agent_name = ''

        if agent_details.find(','):
            agent_name = agent_details[:agent_details.find(',')]
        else:
            raise exceptions.UnrecognizedAgentNameFormat('Could not process agent, unrecognized name pattern!')
        return agent_name

    def get_property_listing_type(self):
        """ Gets the type of property advertised on the site: for sale or to rent.
        """
        soup_obj = self._get_html_content()
        property_type = re.search(r'Property\s(\w+\s\w+)\s', soup_obj.title.text).group(1)
        return property_type.title()

    def get_date_properties_added(self):
        """ Gets the number of properties added to the site per date.
        """
        soup_obj = self._get_html_content()
        count_properties_added_per_date = {}

        all_date_tags = soup_obj.findAll('strong', {'class': 'listing_sort_copy'})
        for dt in all_date_tags:
            date_added = re.search(r'(\d{1,2}\w{2}\s\w+\s\d{4})', dt.text).group()
            if date_added in count_properties_added_per_date:
                count_properties_added_per_date[date_added] += 1
            else:
                count_properties_added_per_date[date_added] = 1
        return count_properties_added_per_date

    def prepare_results(self):
        """ stores the results of crawling a specific page to the base class list attribute.
        """
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
