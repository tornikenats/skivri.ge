FROM python:alpine

COPY scraper /scraper
COPY run.py /run.py
COPY requirements/requirements.txt /scraper/requirements.txt

RUN apk add --update --no-cache g++ gcc libxslt-dev libxml2-dev

RUN pip install -r /scraper/requirements.txt

CMD ["python", "run.py"]