FROM ubuntu:16.04

MAINTAINER IwiKoRa

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

COPY ./requirements.txt /server/requirements.txt

WORKDIR /server

RUN pip install -r requirements.txt

COPY . /server

ENV FLASK_APP index.py
ENV FLASK_ENV development

EXPOSE 80


CMD ["flask","run","--host=0.0.0.0", "--port=80"]
