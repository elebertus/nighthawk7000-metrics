#!/bin/sh
echo "starting metrics loop"
while true; do
  echo "in metrics loop"
  /opt/app/metrics_collector.py
  sleep 10
done
