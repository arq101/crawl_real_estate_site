#!/usr/bin/env python
# -*- coding: utf-8 -*-

from source import crawl_webpage
from configs import config


def run_crawler():
    for url in config.URL_ADDR:
        crawler = crawl_webpage.Crawler(url)
        crawler.print_results()


def main():
    run_crawler()


if __name__ == '__main__':
    main()