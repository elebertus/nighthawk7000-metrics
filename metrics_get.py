#!./venv/bin/python3
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import os
import sys


def get_config():
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


def log_error(e):
    print(e)


def get_metrics(config):

    print(config)
    metric_request = simple_get(config)

    if not metric_request:
        log_error("Error collecting metrics")

    soup = BeautifulSoup(metric_request, 'html.parser')
    metric_list = []
    table = soup.find('table', attrs={'border': '1', 'cellpadding': '0', 'cellspacing':'0', 'width': '99%'})
    trs = table.find_all('tr')
    
    for tr in trs:
        tds = tr.find_all('td')
        tds = [ele.text.strip() for ele in tds]
        metric_list.append([ele for ele in tds if tds])

    return metric_list
    #for s in d:
    #    print(s)
