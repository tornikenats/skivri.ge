FROM python:alpine

COPY backend /backend
COPY autoapp.py /autoapp.py
COPY requirements/requirements.txt /backend/requirements.txt

RUN pip install -r backend/requirements.txt

CMD ["gunicorn", "-w 1", "-b :5010", "autoapp:app"]