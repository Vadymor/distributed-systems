FROM python:3.10

WORKDIR /code

COPY Pipfile ./
COPY Pipfile.lock ./

RUN pip install pipenv
RUN set -ex && pipenv install --system

COPY ./code/ ./code