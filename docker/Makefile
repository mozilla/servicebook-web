.PHONY: build run

build:
	docker build -t serviceweb/dev:latest .

run:
	docker run -p 127.0.0.1:5000:80 serviceweb/dev

attach:
	docker exec -i -t $(ID) /bin/bash
