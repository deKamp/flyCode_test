FROM python:3.7-slim-stretch

# Точка монтирования БД
VOLUME /srv/db

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential libffi-dev locales-all

RUN pip install --upgrade pip

ADD requirements.txt /

RUN pip install -r /requirements.txt

WORKDIR /srv
ADD Library/ /srv
