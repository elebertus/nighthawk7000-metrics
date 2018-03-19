#!./venv/bin/python3

import metrics_get as m
#import signal_handler


def main():
    config = m.get_config()
    metrics = m.get_metrics(config)

    for metric in metrics:
        print(metric)

main()