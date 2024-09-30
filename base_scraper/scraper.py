from abc import ABC, abstractmethod


class BaseScraper(ABC):
    def __init__(self):
        self.urls = []

    @abstractmethod
    def scrape(self, urls):
        pass

    @abstractmethod
    def parse(self, response):
        pass
