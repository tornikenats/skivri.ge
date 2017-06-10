FROM python:alpine

COPY . /scraper
WORKDIR /scraper

RUN apk add --update --no-cache g++ gcc libxslt-dev

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["main.py"]