from datetime import datetime, timezone


def validate_article_row(article_row):
    # ensure any article erroneously dated in the future is re-dated to now
    now = datetime.utcnow()
    now = now.replace(tzinfo=timezone.utc)
    if article_row['date_pub'] > now:
        article_row['date_pub'] = now

    return article_row
