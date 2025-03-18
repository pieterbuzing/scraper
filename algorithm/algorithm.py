from time import sleep

import settings
from scrapers.scraper import Scraper
from sinks.sink import Sink


class Algorithm:

    def __init__(self, scraper: Scraper):
        """ Create an algorithm that iteratively scrapes a site and stores the result.
        :param scraper: The scraper to use
        """
        assert scraper is not None
        self.scraper = scraper
        self.sinks = []
        self.running = False

    def add_sink(self, sink: Sink):
        """ Add a sink to the list of sinks that the result is sent to.
        :param sink: the new sink
        """
        self.sinks.append(sink)

    def start(self):
        """ Start the algorithm.
        """
        self.running = True
        while self.running:
            data = self.scraper.scrape()
            for sink in self.sinks:
                sink.update(data)
            sleep(settings.ALGORITHM_SLEEP_TIME)

    def stop(self):
        """ Stops the algorithm.
        Note: this is not supported yet.
        """
        assert False
        # self.running = False
