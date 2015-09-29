#!/usr/bin/env python
# -*- coding: utf-8 -*-

from source import crawl_webpage_zoopla, crawl_webpage_rightmove, crawling_results
from configs import config


def run_crawler():
    for url in config.URL_ADDR:
        if url.startswith('http://www.zoopla.co.uk'):
            crawler = crawl_webpage_zoopla.CrawlZooplaSite(url)
            crawler.prepare_results()
        elif url.startswith('http://www.rightmove.co.uk'):
            crawler = crawl_webpage_rightmove.CrawlRightMoveSite(url)
            crawler.prepare_results()


def print_results():
    res = crawling_results.CrawlerResults()
    res.display_all_results()
    res.search_and_display_by_agent('House Network')


def main():
    run_crawler()
    print_results()


if __name__ == '__main__':
    main()