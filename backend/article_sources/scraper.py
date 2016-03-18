import model.articles as articles
import config


class Scraper:
    ArticlesTable = articles.initialize(config.settings['MYSQL_DB'],
                                        config.settings['MYSQL_USER'],
                                        config.settings['MYSQL_PASS'])

    def __init__(self, name):
        self.name = name

    def fetch(self):
        raise NotImplemented