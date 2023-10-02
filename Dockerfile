FROM python:slim-bookworm

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r ./requirements.txt

RUN apt-get update \
    && apt-get -y install libpq-dev gcc


COPY . .