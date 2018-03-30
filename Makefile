.PHONY: build run

build:
	docker build -t nighthawk-r7000-metrics .

run:
	docker rm -f nighthawk-r7000-metrics; docker run -d -eMETRICS_USER=${METRICS_USER} -eMETRICS_PASSWORD=${METRICS_PASSWORD} -eMETRICS_URL=${METRICS_URL} nighthawk-r7000-metrics

