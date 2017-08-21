.PHONY: build run

SERVICEBOOK = http://192.168.1.12:5000/api/

build:
	docker build -t serviceweb/dev:latest .

run:
	docker run -p 127.0.0.1:5000:5000 -e SERVICEBOOK=$(SERVICEBOOK) serviceweb/dev

attach:
	docker exec -i -t $(ID) /bin/bash
