import html
import logging
import re
from collections import OrderedDict

import settings
from scrapers.scraper import Scraper
import requests
from bs4 import BeautifulSoup, Tag

PARSER = "html.parser"


class Scraper112app(Scraper):

    def __init__(self, url: str = None):
        self.url = url or settings.SCRAPER_URL.format(settings.SCRAPER_REGION)
        logging.debug(f"Scraper112app.__init__(): url= {self.url}")

    def scrape(self) -> [OrderedDict]:
        page = requests.get(self.url)
        logging.debug(f"page status: {page.status_code}")

        soup = BeautifulSoup(page.content, PARSER)

        result = []
        links = soup.findAll('a', class_="m_title_link")
        for link in links[:3]:
            suburl = link.get("href")
            try:
                dict = OrderedDict()
                dict["id"] = re.search("melding\/(\d+)$", suburl)[1]
                self._scrape_sub_page(suburl, dict)
                result.append(dict)
            except ValueError as e:
                logging.error(f"Error parsing sub page {suburl}:\n{str(e)}")

        return result

    def _scrape_sub_page(self, url: str, d: OrderedDict):
        sub_soup = BeautifulSoup(requests.get(url).content, PARSER)
        h3 = self._find_first_element(sub_soup, "h3", class_="m_title")

        d["text"] = h3.contents[0]

        h6 = self._find_first_element(h3.parent, 'h6')
        if h6:
            d["time_text"] = h6.contents[0]
            info = self._find_first_element(h6, "span", class_="badge-info")
            d["priority"] = info.contents[0] if info else ""
            primary = self._find_first_element(h6, "span", class_="badge-primary")
            d["vehicle"] = primary.contents[0] if primary else ""

        cap_links = h3.parent.find_all("a", class_="cap_link")
        cap_str = ", ".join([cap.contents[0] for cap in cap_links])
        d["caps"] = cap_str

        cap_spans = h3.parent.find_all("span", class_="m_soort_a")
        cap_types = ", ".join([cap.next.next.strip() for cap in cap_spans])
        d["types"] = cap_types

        latitude, longitude = self._get_lat_lng(sub_soup)
        d["lat"] = latitude
        d["lng"] = longitude
        d["street"], d["city"] = self._get_street_number_city(sub_soup)
        return d

    def _find_first_element(self, tag: Tag, element: str, class_: str = None):
        if class_:
            children = tag.findAll(element, class_=class_)
        else:
            children = tag.findAll(element)

        if len(children) == 0:
            return None
        return children[0]

    def _get_street_number_city(self, soup):
        street, city = None, None
        map_divs = soup.find_all("div", id="m_map")
        if len(map_divs) > 0:
            par = map_divs[0].parent
            for div in par.find_all("div"):
                if len(div.contents) == 2 and div.contents[0].startswith("Locatie:"):
                    text = div.contents[1].contents[0]
                    address_city = text.split(",")
                    if len(address_city) > 1:
                        city = address_city[-1].strip()
                        street = address_city[0].strip()
        return street, city

    def _get_lat_lng(self, soup):
        latitude, longitude = None, None
        map_divs = soup.find_all("div", id="m_map")
        if len(map_divs) > 0:
            par = map_divs[0].parent
            scripts = par.find_all("script")
            if len(scripts) > 0:
                text = scripts[0].string
                m_lat = re.findall('lat: (\d+\.\d+)', text, flags=re.MULTILINE)
                if m_lat and len(m_lat) == 1:
                    latitude = float(m_lat[0])
                m_lng = re.findall('lng: (\d+\.\d+)', text, flags=re.MULTILINE)
                if m_lng and len(m_lng) == 1:
                    longitude = float(m_lng[0])
        return latitude, longitude

