# Servicebook
FROM python:3.5-slim
WORKDIR /app
COPY version.json version.json
RUN cat version.json
RUN mkdir -p /etc/dpkg/dpkg.cfg.d \
    &&  echo "path-exclude=/usr/share/locale/*" >> /etc/dpkg/dpkg.cfg.d/excludes \
    &&  echo "path-exclude=/usr/share/man/*" >> /etc/dpkg/dpkg.cfg.d/excludes \
    &&  echo "path-exclude=/usr/share/doc/*" >> /etc/dpkg/dpkg.cfg.d/excludes \
    &&  apt-get -qq update \
    &&  apt-get -y install --no-install-recommends \
        build-essential \
        libffi-dev \
        libssl-dev \
        curl \
        git \
        supervisor \
        vim-tiny \
    && rm -rf /var/lib/apt/lists/* /usr/share/doc/* /usr/share/man/* /usr/share/locale/*

RUN addgroup --gid 10001 app
RUN adduser --gid 10001 --uid 10001 --home /app --shell /sbin/nologin --no-create-home --disabled-password --gecos we,dont,care,yeah app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY supervisor.conf /etc/supervisor/conf.d/
ADD . /app
COPY entrypoint.sh /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["start"]
EXPOSE 5000
