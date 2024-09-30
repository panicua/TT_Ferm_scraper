"""
Main script for scraping fungicides tab from https://agroplant.com.ua/uk/.

Reads URLs from an Excel file, transforms them into a list and
scrapes the data using the FungicideScraper at the end saves it to a CSV file.
"""

from fungicide_scrapers.scraper import FungicideScraper
from utils.format_utils import excel_to_df, df_to_list
from decouple import config
import asyncio


async def main():
    scraper = FungicideScraper()
    urls = df_to_list(
        excel_to_df(
            f"../excel_files_to_scrape/{config('EXCEL_WITH_LINKS')}"
        )[config("EXCEL_LINKS_COLUMN_NAME")]
    )
    df = await scraper.scrape(urls)
    df.to_csv("../results/fungicides_data.csv", index=False)

if __name__ == "__main__":
    asyncio.run(main())
