FROM python:alpine

COPY scraper /scraper
COPY wait-for.sh /wait-for.sh
WORKDIR /scraper

RUN apk add --update --no-cache g++ gcc libxslt-dev libxml2-dev

RUN pip install -r requirements.txt

CMD ["/wait-for.sh", "db:3306", "--", "python", "main.py"]