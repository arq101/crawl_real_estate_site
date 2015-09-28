from BeautifulSoup import BeautifulSoup
import requests
import re

import exceptions


class Crawler(object):
    """ Class offers methods to crawl real estate website and display:
    agent name,
    date property was added to site,
    & property type; to-rent or for-sale
    """

    def __init__(self, url_addr):
        self.url_addr = url_addr

    def _get_html_content(self):
        """ Extracts the html from the web-page of a given url.

        :return: BeautifulSoup object
        """
        try:
            response = requests.get(self.url_addr)
        except requests.exceptions.ConnectionError as e:
            raise exceptions.ConnectionError(e)
        except requests.exceptions.HTTPError as e:
            raise exceptions.ConnectionError(e)
        except requests.exceptions.Timeout as e:
            raise exceptions.ConnectionError(e)
        else:
            data = response.text
            return BeautifulSoup(data)

    def get_agents(self):
        """ Gets the names of the agents that uploaded the property to the site.

        :return: list with agent names.
        """
        soup_obj = self._get_html_content()
        agent_names = []
        agents = soup_obj.findAll('div', {'class': 'agent_logo'})

        agent_regex_single_name = re.compile(r'alt="Marketed by (\w+),')
        agent_regex_double_name = re.compile(r'alt="Marketed by (\w+\s\w*)')
        for tag_line in agents:
            if agent_regex_single_name.search(tag_line.renderContents()):
                agent_names.append(agent_regex_single_name.search(tag_line.renderContents()).group(1))
            elif agent_regex_double_name.search(tag_line.renderContents()):
                agent_names.append(agent_regex_double_name.search(tag_line.renderContents()).group(1))
            else:
                raise exceptions.UnrecognizedAgentNameFormat('Could not process agent, unrecognized name pattern!')
        return agent_names

    def get_date_added(self):
        """ Get the date for which a property was added to the site.

        :return: list of the added dates
        """
        soup_obj = self._get_html_content()
        property_advertised_dates = []

        date_added = soup_obj.findAll('strong', {'class': 'listing_sort_copy'})
        for tag_line in date_added:
            property_advertised_dates.append(re.search(r'\d{2}\w{2}\s\w+\s\d{4}', tag_line.contents[0]).group(0))
        return property_advertised_dates
    
    def get_property_category(self):
        """ Gets the type of property advertised on the site: for-sale or to-rent.

        :return: a list of property type
        """
        soup_obj = self._get_html_content()
        property_categories = []
        
        category = soup_obj.findAll('span', {'class': 'agent_phone'})
        for tag_line in category:
            if re.search(r'data-ga-category="Lead single \(for-sale\)', tag_line.renderContents()):
                property_categories.append('for-sale')
            elif re.search(r'data-ga-category="Lead single \(to-rent\)', tag_line.renderContents()):
                property_categories.append('To-Rent')
            else:
                property_categories.append('Unknown')
        return property_categories

    def print_results(self):
        agents = self.get_agents()
        dates_added = self.get_date_added()
        property_categories = self.get_property_category()

        if not agents and not dates_added and property_categories:
            raise exceptions.NoDataError("No relevant data was found from the given webpage(s)!")

        for agent, dt, category in zip(agents, dates_added, property_categories):
            print '{0}, {1}, {2}'.format(agent, dt, category)





