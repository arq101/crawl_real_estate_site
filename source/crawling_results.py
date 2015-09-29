# -*- coding: utf-8 -*-
from operator import itemgetter

from base import Base


class CrawlerResults(Base):

    def display_all_results(self):
        print "\n>> Retrieving all results ..."
        sorted_list = sorted(Base.list_results, key=itemgetter('date'))
        for d_item in sorted_list:
            print "{0:<20} {1:<20} {2:<20} {3:<20}".format(
                d_item['agent'], d_item['date'], d_item['type'], d_item['properties_added'])

    def search_and_display_by_agent(self, agent):
        print "\n>> Searching for agent: {} ...".format(agent)
        counter = 0
        for d_item in Base.list_results:
            if agent == d_item['agent']:
                counter += 1
                print "{0:<20} {1:<20} {2:<20} {3:<20}".format(
                    d_item['agent'], d_item['date'], d_item['type'], d_item['properties_added'])

            if counter == 0:
                print "Did not find results for agent name: {}!".format(agent)
