#!/bin/sh
while true; do
  METRICS_USER=$METRICS_USER METRICS_PASSWORD=$METRICS_PASSWORD METRICS_URL=$METRICS_URL /opt/app/metrics_collector.py
  sleep 10
done
