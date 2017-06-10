from peewee import fn, JOIN
from playhouse.shortcuts import model_to_dict
from skivrige_model import Articles
from datetime import datetime
import json


def get_all_articles(language):
    return Articles \
        .select() \
        .where(Articles.lang == language) \
        .order_by(Articles.date_pub.desc())