import asyncio
import random

import aiohttp
import pandas as pd
from bs4 import BeautifulSoup

from agroplant.fungicide_scrapers.constants import (
    PRODUCT_PAGE_CHECK,
    PRODUCT_PRICE_CLASS,
    PRODUCT_AVAILABILITY_SELECTOR,
    PRODUCT_NAME_CLASS,
    PRODUCT_MANUFACTURER_SELECTOR,
    PRODUCT_FORM_OUTER_CLASS_VARIANT_1,
    PRODUCT_FORM_OUTER_CLASS_VARIANT_2,
    PRODUCT_FORM_INNER_CLASS,
)
from base_scraper.scraper_interface import BaseScraper
from utils.constants import HEADERS
from utils.user_agents import USER_AGENTS


class FungicideScraper(BaseScraper):
    async def send_request(
            self,
            session,
            url,
            retries=3,
            delay=5
    ) -> str | None:
        headers = {**HEADERS, "User-Agent": random.choice(USER_AGENTS)}
        for attempt in range(retries):
            try:
                timeout = aiohttp.ClientTimeout(total=30)
                async with session.get(
                    url, headers=headers, timeout=timeout
                ) as response:
                    if response.status == 200:
                        return await response.text()
                    else:
                        print(
                            f"Skipping {url} due to invalid response or "
                            f"status code: {response.status}"
                        )
                        return None
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                print(f"Attempt {attempt + 1} failed for {url}: {e}")
                if attempt < retries - 1:
                    await asyncio.sleep(delay)
                else:
                    return None

    async def scrape(self, urls: list[str]) -> pd.DataFrame:
        async with aiohttp.ClientSession() as session:
            tasks = [self.validate_and_parse_url(session, url) for url in urls]
            try:
                results = await asyncio.gather(
                    *tasks, return_exceptions=True
                )
            except asyncio.CancelledError:
                print("Task was cancelled")
                return pd.DataFrame()

        data = []
        for result in results:
            # Ensure that result is not an exception
            if isinstance(result, Exception):
                print(f"Error occurred: {result}")
                continue

            # Ensure that result is not None or invalid
            if not result:
                continue

            # Safely extract product details from result
            product_values = {
                "url": result.get("url"),
                "price": self._get_price(result.get("soup")),
                "availability": self._get_availability(result.get("soup")),
                "product_name": self._get_product_name(result.get("soup")),
                "manufacturer": self._get_manufacturer(result.get("soup")),
                "product_form": self._get_product_form(result.get("soup")),
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
                "product_form",
            ],
        )

    async def validate_and_parse_url(
            self,
            session: aiohttp.ClientSession,
            url: str
    ) -> dict | None:
        """
        Validates the URL and parses it if valid.
        Returns parsed data or None if the URL is invalid.
        """
        response = await self.send_request(session, url)

        if not response:
            return None

        # Parse response with BeautifulSoup
        soup = BeautifulSoup(response, "lxml")

        # Validate the presence of element that product must have
        if soup.find("div", class_=PRODUCT_PAGE_CHECK) is None:
            print(f"Skipping {url} due to missing product price element")
            return None

        # Proceed to parsing if valid
        print(f"Valid product page found at {url}")
        return {"url": url, "soup": soup}

    def _get_price(self, soup: BeautifulSoup) -> str:
        """
        Extracts the price string from the given HTML.

        :param soup: Parsed HTML of the product page.
        :return: Price string. E.g. "6 680 грн."
        """
        element = soup.find(
            "div", class_=PRODUCT_PRICE_CLASS
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
            PRODUCT_AVAILABILITY_SELECTOR
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
        element = soup.find("div", class_=PRODUCT_NAME_CLASS)
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
            PRODUCT_MANUFACTURER_SELECTOR
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
        all_attributes = (
            soup.find_all("div", class_=PRODUCT_FORM_OUTER_CLASS_VARIANT_1)
            or soup.find_all("div", class_=PRODUCT_FORM_OUTER_CLASS_VARIANT_2)
        )

        for attribute in all_attributes:
            if any(key in attribute.text for key in (
                    "Тара", "Тарна одиниця", "Упаковка",
            )):
                element = attribute.find(
                    "span", class_=PRODUCT_FORM_INNER_CLASS
                )
                if element:
                    return element.text.strip()

                second_variant_elements = attribute.select("ul li")
                for second_variant_element in second_variant_elements:
                    if any(key in second_variant_element.text for key in (
                            "Тара", "Тарна одиниця", "Упаковка",
                    )):
                        return "".join(
                            second_variant_element.text.strip().split()[1:]
                        )
                return "Unknown"
        return "Unknown"
