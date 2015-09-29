# -*- coding: utf-8 -*-
import unittest
from BeautifulSoup import BeautifulSoup

from source import crawl_webpage


class TestCrawlWebPage(unittest.TestCase):

    def test_get_html_content_success(self):
        crl = crawl_webpage.Crawler('http://www.google.com')
        response = crl._get_html_content()
        self.assertIsInstance(response, BeautifulSoup)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
