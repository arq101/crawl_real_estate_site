# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
import requests

import exceptions
from base import Base


class Crawler(Base):
    """ Class offers method to crawl real estate website and
    retrieve the HTML content.
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
