FROM python:alpine

COPY ./application /application
COPY skivrige_model /skivrige_model
COPY wait-for.sh /wait-for.sh
WORKDIR /application

RUN pip install -r requirements.txt
RUN pip install /skivrige_model

EXPOSE 5000

CMD ["/wait-for.sh", "db:3306", "--", "gunicorn", "-w 3", "-b :5000", "autoapp:app"]