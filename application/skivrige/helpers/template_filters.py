import datetime
import re

def timedelta(pub_date):
    delta = datetime.datetime.utcnow() - pub_date

    secs = delta.total_seconds()
    days, remainder = divmod(secs, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    days_str = ''
    if days != 0:
        days_str = '{:0.0f} day'.format(days)
        if days > 1: days_str += 's'
        days_str += ', '

    hours_str = ''
    if hours != 0:
        hours_str = '{:0.0f} hour'.format(hours)
        if hours > 1: hours_str += 's'
        hours_str += ', '

    minutes_str = ''
    if minutes != 0:
        minutes_str = '{:0.0f} minute'.format(minutes)
        if minutes > 1: minutes_str += 's'
        minutes_str += ', '
    else:
        minutes_str = 'seconds'

    delta_str = '{}{}{}'.format(days_str, hours_str, minutes_str)
    return delta_str.strip(', ') + ' ago'


def removetags(text):
    TAG_RE = re.compile(r'<[^>]+>')
    return TAG_RE.sub('', text)
