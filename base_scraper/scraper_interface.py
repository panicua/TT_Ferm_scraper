from abc import ABC, abstractmethod


class BaseScraper(ABC):
    @abstractmethod
    def send_request(self, *args, **kwargs):
        """Sends an HTTP GET request to the given URL."""
        pass

    @abstractmethod
    def scrape(self, *args, **kwargs):
        """Scrapes the data from the given URLs."""
        pass
