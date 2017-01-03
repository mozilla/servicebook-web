# Servicebook
FROM python:3-slim

ADD . /code
RUN \
    apt-get update; \
    apt-get install -y python3-pip python3-venv git build-essential make; \
    apt-get install -y python3-dev libssl-dev libffi-dev

RUN \
    pip install -e /code ; \


EXPOSE 5000
CMD serviceweb
