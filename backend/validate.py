from datetime import datetime, timezone


def validate_article_row(article_row):
    now = datetime.utcnow()
    now = now.replace(tzinfo=timezone.utc)
    if article_row['date_pub'] > now:
        article_row['date_pub'] = now

    return article_row
