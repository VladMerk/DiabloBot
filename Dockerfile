FROM python:3-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

ADD requirements.txt /app/

RUN apk upgrade
RUN apk add git
RUN python -m pip install -U pip setuptools -r requirements.txt

COPY ./src/ /app/
