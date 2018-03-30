#!/usr/bin/env python3

import metrics_get as m
from telegraf_client import Telegraf

def main():
  config = m.get_config()
  metrics = m.get_metrics(config)

  for metric in metrics:
    t = Telegraf("12.12.12.7", "8094", "tcp")
    t.metric(metric)
    t.send_metric()




# TODO: This will eventually be called in a loop, or meant to be able to be 
# daemonized
main()