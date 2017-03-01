.PHONY: build run

SERVICEBOOK = http://192.168.1.101:5001/api/

build:
	docker build -t serviceweb/dev:latest .

run:
	docker run -p 127.0.0.1:5000:80 -e SERVICEBOOK=$(SERVICEBOOK) serviceweb/dev

attach:
	docker exec -i -t $(ID) /bin/bash
