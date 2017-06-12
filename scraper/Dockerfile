FROM python:alpine

COPY scraper /scraper
COPY skivrige_model /skivrige_model
COPY wait-for.sh /wait-for.sh
WORKDIR /scraper

RUN apk add --update --no-cache g++ gcc libxslt-dev libxml2-dev

RUN pip install -r requirements.txt
RUN pip install /skivrige_model

CMD ["/wait-for.sh", "db:3306", "--", "python", "main.py"]