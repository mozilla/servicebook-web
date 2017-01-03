# Servicebook
FROM python:3-slim

RUN \
    apt-get update; \
    apt-get install -y python3-pip python3-venv git build-essential make; \
    apt-get install -y python3-dev libssl-dev libffi-dev


ADD ./requirements.txt /code/requirements.txt
RUN pip install -r /code/requirements.txt

ADD . /code
RUN cd /code; python setup.py develop

EXPOSE 5000
CMD serviceweb
