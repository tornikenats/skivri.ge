FROM python:alpine

COPY . /app
# COPY autoapp.py autoapp.py
WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["gunicorn"]
CMD ["-w 3", "-b :5000", "autoapp:app"]