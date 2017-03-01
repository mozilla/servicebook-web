# Servicebook
FROM python:3.5-slim

WORKDIR /app
RUN apt-get update
RUN apt-get install git -y
RUN apt-get install build-essential -y
RUN apt-get install nginx supervisor -y
# for debugging within the docker container
RUN apt-get install vim curl -y
RUN rm -rf /var/lib/apt/lists/*

RUN addgroup --gid 10001 app
RUN adduser --gid 10001 --uid 10001 --home /app --shell /sbin/nologin --no-create-home --disabled-password --gecos we,dont,care,yeah app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY nginx.conf /etc/nginx/sites-available/default
COPY global-nginx.conf /etc/nginx/nginx.conf

COPY supervisor.conf /etc/supervisor/conf.d/
COPY version.json /app/version.json

ADD . /app
EXPOSE 80
CMD supervisord -n
