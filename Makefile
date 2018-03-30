.PHONY: build run stop

build:
	docker build -t nighthawk-r7000-metrics .

metrics_user := ${METRICS_USER}
metrics_password := ${METRICS_PASSWORD}
metrics_url := ${METRICS_URL}

run:
	docker rm -f nighthawk-r7000-metrics; docker run -d --name nighthawk-r7000-metrics -eMETRICS_USER=$$METRICS_USER -eMETRICS_PASSWORD=$$METRICS_PASSWORD -eMETRICS_URL=$$METRICS_URL nighthawk-r7000-metrics /opt/app/run_metrics.sh

stop:
	docker stop nighthawk-r7000-metrics
