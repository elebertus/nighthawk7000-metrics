#!./venv/bin/python3

from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

import os
import sys


def get_config():
        # TODO: I'm not sure if this is a scope problem or something else, but if these vars
        # aren't exported, then `soup = BeautifulSoup()` gets parsed before these if blocks
        # Probably just move this into a configure package and have it read json or whatever
        # the common python format is.
        config = {}
        if os.getenv('METRICS_USER'):
            config['metrics_user'] = os.environ['METRICS_USER']
        else:
            log_error("Export the METRICS_USER environment variable.")
            sys.exit(1)
        
        if os.getenv('METRICS_PASSWORD'):
            config['metrics_password'] = os.environ['METRICS_PASSWORD']
        else:
            log_error("Export the METRICS_PASSWORD environment variable.")
            sys.exit(1)

        if os.getenv('METRICS_URL'):
            config['metrics_url'] = os.environ['METRICS_URL']
        else:
            log_error("Export the METRICS_URL environment variable.")
            sys.exit(1)

        return config 


def simple_get(config):
    try:
        with closing(get(config['metrics_url'], stream=True, auth=(config['metrics_user'], config['metrics_password']))) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error("Error during requests to {0} : {1}".format(url,str(e)))


def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1 )


# TODO: Does python have a logging library?
def log_error(e):
    print(e)


def get_metrics(config):

    metric_request = simple_get(config)

    if not metric_request:
        # TODO: Bubble up and error to the caller and handle it
        log_error("Error collecting metrics")

    soup = BeautifulSoup(metric_request, 'html.parser')
    metric_list = []
    table = soup.find('table', attrs={'border': '1', 'cellpadding': '0', 'cellspacing':'0', 'width': '99%'})
    trs = table.find_all('tr')
    
    for tr in trs:
        tds = tr.find_all('td')
        tds = [ele.text.strip() for ele in tds]
        metric_list.append([ele for ele in tds if tds])

    return telegraf_format_metrics(metric_list)
    #for s in d:
    #    print(s)


def telegraf_format_metrics(metric):
    """
     WAN and the wireless both have full metrics but LAN is an aggregate for rates
     each individual port has their own Up Time.
    { 'Collisions': '0',
      'Port': 'WAN',
      'Rx B/s': '19783',
      'RxPkts': '29421179',
      'Status': '1000M/Full',
      'Tx B/s': '22886',
      'TxPkts': '12114689',
      'Up Time': '2 days 03:06:30'}
    { 'Collisions': '0',
      'Port': 'LAN1',
      'Rx B/s': '215',
      'RxPkts': '223672691',
      'Status': '100M/Full',
      'Tx B/s': '329',
      'TxPkts': '351957437',
      'Up Time': '53 days 21:45:15'}
    {'Port': 'LAN2', 'Status': '1000M/Full', 'TxPkts': '03:24:06'}
    {'Port': 'LAN3', 'Status': '1000M/Full', 'TxPkts': '2 days 08:53:34'}
    {'Port': 'LAN4', 'Status': '1000M/Full', 'TxPkts': '36 days 03:07:26'}
    { 'Collisions': '0',
      'Port': '2.4G WLAN b/g/n',
      'Rx B/s': '96',
      'RxPkts': '47423414',
      'Status': '600M',
      'Tx B/s': '408',
      'TxPkts': '88949072',
      'Up Time': '90 days 14:01:10'}
    { 'Collisions': '0',
      'Port': '5G WLAN a/n/ac',
      'Rx B/s': '456',
      'RxPkts': '334657697',
      'Status': '1300M',
      'Tx B/s': '324',
      'TxPkts': '1313778633',
      'Up Time': '90 days 14:01:10'}

    """
    # TODO: Throw away the Up Time metric for the LAN interfaces and munge them into one just keeping the metrics
    # and convert the Up Time into hours using datetime.striptime()
    # The metrics-collector module should also handle the sending and calling of Telegraf
    # so we can handle formating these into Telegraf.metric()
    keys = metric.pop(0)
    mv = []
    for m in metric:
        mv.append(dict(zip(keys, m)))

    return mv


