FROM python:3.11-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone


WORKDIR /app

ADD requirements.txt /app/

RUN apk update && apk upgrade
RUN apk add git sqlite
RUN python -m pip install -U pip setuptools -r requirements.txt

COPY ./src/ /app/
