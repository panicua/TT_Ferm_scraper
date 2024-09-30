from abc import ABC, abstractmethod


class BaseScraper(ABC):
    @abstractmethod
    def send_request(self, url: str):
        """Sends an HTTP GET request to the given URL."""
        pass

    @abstractmethod
    def scrape(self, urls: list[str]):
        pass
