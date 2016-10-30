import logging
import sys
import config

logging.basicConfig(stream=sys.stdout, level=config.log_level)