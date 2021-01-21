FROM python:3.9.1-alpine3.12

WORKDIR /home/app

RUN pip install flask flask-mail Celery

COPY main.py .

CMD flask run --host=0.0.0.0
