FROM python:3.10

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN apt-get update && apt-get install -y postgresql-client

COPY . /app

WORKDIR /app

RUN mkdir -p media
RUN chmod -R 777 media

RUN mkdir -p logs
RUN chmod -R 777 logs

RUN chmod 600 ssl/key.pem ssl/cert.pem

RUN pip install pipenv
RUN pip install -r requirements.txt