FROM python:3.7-slim-stretch

# Точка монтирования для БД
VOLUME /srv/db

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential libffi-dev locales-all

RUN pip install --upgrade pip

ADD requirements.txt /

RUN pip install --no-cache-dir -r /requirements.txt

WORKDIR /srv
ADD Library/ /srv

#Запуск:
#docker run -v <путь до БД>:/srv/db -p "8000:8000" -ti dekamp/proba_django ./manage.py runserver 0.0.0.0:8000