.PHONY: build run

SERVICEBOOK ?= http://192.168.1.12:5000/api/

docker-build:
	docker build -t serviceweb/dev:latest .

docker-run:
	docker run -it -p 127.0.0.1:5000:5000 -e SERVICEBOOK=$(SERVICEBOOK) serviceweb/dev

docker-attach:
	docker exec -i -t $(ID) /bin/bash
