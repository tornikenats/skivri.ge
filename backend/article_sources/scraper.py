import config


class Scraper:
    def __init__(self, name):
        self.name = name

    def fetch(self):
        raise NotImplemented