#!./venv/bin/python3

import metrics_get as m

import pprint


def main():
    config = m.get_config()
    metrics = m.get_metrics(config)


    for metric in metrics:
        print(metric)



# TODO: This will eventually be called in a loop, or meant to be able to be daemonized
main()