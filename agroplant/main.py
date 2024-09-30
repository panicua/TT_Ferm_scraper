"""
Main script for scraping fungicides tab from https://agroplant.com.ua/uk/.

Reads URLs from an Excel file, transforms them into a list and
scrapes the data using the FungicideScraper at the end saves it to a CSV file.
"""

from fungicide_scrapers.scraper import FungicideScraper
from utils.format_utils import excel_to_df, df_to_list

if __name__ == "__main__":
    scraper = FungicideScraper()
    urls = df_to_list(
        excel_to_df(
            "../excel_files_to_scrape/посилання для скачування 1.xlsx")["Ссылки"]
    )
    df = scraper.scrape(urls)
    df.to_csv("fungicides_data.csv", index=False)
