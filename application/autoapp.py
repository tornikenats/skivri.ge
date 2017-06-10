from flask.helpers import get_debug_flag

from skivrige.app import create_app
from skivrige.settings import DevConfig, ProdConfig

CONFIG = DevConfig if get_debug_flag() else ProdConfig

app = create_app(CONFIG)