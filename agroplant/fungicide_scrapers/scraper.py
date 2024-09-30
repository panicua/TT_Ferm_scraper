import random

import pandas as pd
import requests
from bs4 import BeautifulSoup

from base_scraper.scraper_interface import BaseScraper
from utils.constants import HEADERS
from utils.user_agents import USER_AGENTS


class FungicideScraper(BaseScraper):
    def send_request(self, url):
        try:
            headers = {**HEADERS,
                       "User-Agent": random.choice(USER_AGENTS)}
            response = requests.get(url, headers=headers)
            return response
        except requests.exceptions.RequestException as e:
            print(f"Error occurred while requesting {url}: {e}")
            return None

    def scrape(self, urls: list[str]) -> pd.DataFrame:
        """
        Scrapes a list of URLs by validating and parsing them.
        """
        data = []
        for url in urls:
            result_soup = self.validate_and_parse_url(url)
            if not result_soup:
                continue

            product_values = {
                "url": url,
                "price": self._get_price(result_soup),
                "availability": self._get_availability(result_soup),
                "product_name": self._get_product_name(result_soup),
                "manufacturer": self._get_manufacturer(result_soup),
                "product_form": self._get_product_form(result_soup),
            }

            data.append(product_values)

        return pd.DataFrame(
            data,
            columns=[
                "url",
                "price",
                "availability",
                "product_name",
                "manufacturer",
                "product_form"
            ]
        )

    def validate_and_parse_url(self, url):
        """
        Validates the URL and parses it if valid.
        Returns parsed data or None if the URL is invalid.
        """
        response = self.send_request(url)

        # Validate if the response is successful
        if not response or response.status_code != 200:
            print(f"Skipping {url} due to invalid response or status code."
                  f"status code: {response.status_code}")
            return None

        # Parse response with BeautifulSoup
        soup = BeautifulSoup(response.text, "lxml")

        # Validate the presence of element that product mustgit  have
        if soup.find("div", class_="ds-product-main-price") is None:
            print(f"Skipping {url} due to missing product price element")
            return None

        # Proceed to parsing if valid
        print(f"Valid product page found at {url}")
        return soup

    def _get_price(self, soup: BeautifulSoup) -> str:
        """
        Extracts the price string from the given HTML.

        :param soup: Parsed HTML of the product page.
        :return: Price string. E.g. "6 680 грн."
        """
        element = soup.find(
            "div",
            class_="ds-price-new fsz-24 fw-700 dark-text"
        )
        if element is None:
            return "Unknown"
        return element.text.strip()

    def _get_availability(self, soup: BeautifulSoup) -> str:
        """
        Extracts the availability string from the given HTML.

        :param soup: Parsed HTML of the product page.
        :return: Availability string. E.g. "В наявності"
        """
        element = soup.select_one(
            "div.ds-product-main-stock.d-flex.align-items-center."
            "justify-content-center.fw-500.br-7"
        )
        if element is None:
            return "Unknown"
        return element.text.strip()

    def _get_product_name(self, soup: BeautifulSoup) -> str:
        """
        Extracts the product name string from the given HTML.

        :param soup: Parsed HTML of the product page.
        :return: Product name string.
        """
        element = soup.find(
            "div",
            class_="col-12 ds-page-title pb-3"
        )
        if element is None:
            return "Unknown"
        return element.text.strip()

    def _get_manufacturer(self, soup: BeautifulSoup) -> str:
        """
        Extracts the manufacturer name string from the given HTML.

        :param soup: Parsed HTML of the product page.
        :return: Manufacturer name string.
        """
        element = soup.select_one(
            "div.ds-product-top-info.d-flex.flex-column."
            "flex-md-row.align-iems-md-center a.blue-link"
        )
        if element is None:
            return "Unknown"
        return element.text.strip()

    def _get_product_form(self, soup: BeautifulSoup) -> str:
        """
        Extracts the product form string from the given HTML.

        :param soup: Parsed HTML of the product page.
        :return: Product form string. E.g. "5л"
        """
        all_attributes = soup.find_all(
            "div",
            class_="ds-product-main-attributes-item br-4 py-1 px-2"
        )

        for attribute in all_attributes:
            if "Тара:" in attribute.text:
                element = attribute.find(
                    "span",
                    class_="fsz-12 fw-500 ps-2"
                )
                if element is None:
                    return "Unknown"
                return element.text.strip()
        return "Unknown"
