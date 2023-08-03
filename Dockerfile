FROM python:slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone


WORKDIR /app

ADD requirements.txt /app/

RUN python -m pip install -U pip setuptools -r requirements.txt

COPY ./src/ /app/
