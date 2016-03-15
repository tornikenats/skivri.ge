import logging
import config

logging.basicConfig(filename=config.path[config.env]['log'], level=logging.DEBUG)