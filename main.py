import logging

from algorithm.algorithm import Algorithm
from scrapers.scraper112app import Scraper112app
from sinks.CSV_Sink import CSV_Sink
from sinks.HTML_Sink import HTML_Sink
from sinks.MySQL_Sink import MySQL_Sink

if __name__ == '__main__':
    logging.basicConfig(filename='scraper.log', level=logging.DEBUG)
    logging.info("starting main!")

    scraper = Scraper112app()
    algo = Algorithm(scraper)
    algo.add_sink(CSV_Sink())
    algo.add_sink(HTML_Sink())
    algo.add_sink(MySQL_Sink())
    algo.start()
