# -*- coding: utf-8 -*-
from operator import itemgetter

from base import Base


class CrawlerResults(Base):
    """ Class offers methods to print results to the terminal.
    """

    _spacing = 20

    def display_all_results(self):
        print "\n>> Retrieving all results from defined urls ..."
        # sort the list of dict objects by the date value within each dict,
        # eg. {'date': '28th Jul 2015', 'properties_added': 1, 'type': u'For Sale', 'agent': u'Settled'},
        sorted_list = sorted(Base.list_results, key=itemgetter('date'))
        for d_item in sorted_list:
            print "{0:<{4}} {1:<{4}} {2:<{4}} {3:<{4}}".format(
                d_item['agent'], d_item['date'], d_item['type'], d_item['properties_added'], self._spacing)

    def search_and_display_by_agent(self, agent):
        print "\n>> Searching for agent: {} ...".format(agent)
        counter = 0
        for d_item in Base.list_results:
            if agent == d_item['agent']:
                counter += 1
                print "{0:<{4}} {1:<{4}} {2:<{4}} {3:<{4}}".format(
                    d_item['agent'], d_item['date'], d_item['type'], d_item['properties_added'], self._spacing)

        if counter == 0:
            print "Did not find results for agent name: {}!".format(agent)
