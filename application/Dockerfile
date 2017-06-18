FROM python:alpine

RUN apk update && \
    apk upgrade && \
    apk add git

ENV prometheus_multiproc_dir /application/skivrige/metrics
RUN rm -f /application/skivrige/metrics/*

COPY ./application /application
COPY skivrige_model /skivrige_model
COPY wait-for.sh /wait-for.sh
WORKDIR /application

RUN pip install -r requirements.txt
RUN pip install /skivrige_model
RUN pip install git+https://github.com/TornikeNatsvlishvili/flask-prometheus.git

EXPOSE 5000

CMD ["/wait-for.sh", "db:3306", "--", "gunicorn", "-w 3", "-b :5000", "autoapp:app"]