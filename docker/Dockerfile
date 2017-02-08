# Servicebook
FROM python:3.5-slim

WORKDIR /app
RUN apt-get update
RUN apt-get install git -y
RUN apt-get install build-essential -y
RUN apt-get install nginx supervisor -y
RUN rm -rf /var/lib/apt/lists/*

RUN addgroup --gid 10001 app
RUN adduser --gid 10001 --uid 10001 --home /app --shell /sbin/nologin --no-create-home --disabled-password --gecos we,dont,care,yeah app


ADD . /app
RUN pip install -r requirements.txt

RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY nginx.conf /etc/nginx/sites-available/default
COPY supervisor.conf /etc/supervisor/conf.d/


EXPOSE 80
CMD supervisord -n
