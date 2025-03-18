from unittest import TestCase

from scrapers.scraper112app import Scraper112app


class TestScraper112app(TestCase):
    def test_scrape(self):
        scraper = Scraper112app(url="http://dataquestio.github.io/web-scraping-pages/simple.html")
        data = scraper.scrape()
        print("data: " + str(data))
