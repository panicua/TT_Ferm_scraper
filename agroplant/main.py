"""
Main script for scraping fungicides tab from https://agroplant.com.ua/uk/.

Reads URLs from an Excel file, transforms them into a list and
scrapes the data using the FungicideScraper at the end saves it to a CSV file.
"""

import asyncio

from agroplant.fungicide_scrapers.settings import (
    EXCEL_WITH_LINKS, EXCEL_LINKS_COLUMN_NAME, CSV_FILE_TO_SAVE
)
from agroplant.fungicide_scrapers.scraper import FungicideScraper
from utils.format_utils import excel_to_df, df_to_list


async def main():
    scraper = FungicideScraper()
    urls = df_to_list(
        excel_to_df(
            f"excel_files_to_scrape/{EXCEL_WITH_LINKS}"
        )[EXCEL_LINKS_COLUMN_NAME]
    )
    df = await scraper.scrape(urls)
    df.to_csv(f"results/{CSV_FILE_TO_SAVE}", index=False)

if __name__ == "__main__":
    asyncio.run(main())
