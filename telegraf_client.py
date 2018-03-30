#!/usr/bin/env python3
import socket


# TODO: General error handling. Need to figure out how we want the 
# caller to do first.
class Telegraf:

    def __init__(self, server, port, proto):
        self.server = server
        self.port = port
        self.proto = proto
        self.line_metric = None
        self.valid_line_metric = None

    def metric(self, metric):

        """
        line format:

          weather,location=us-midwest temperature=82 1465839830100400200
            |    -------------------- --------------  |
            |             |             |             |
            |             |             |             |
          +-----------+--------+-+---------+-+---------+
          |measurement|,tag_set| |field_set| |timestamp|
          +-----------+--------+-+---------+-+---------+
        """

        m = self.to_line_format_string(metric)
        if m != '':
            self.line_metric = m
            self.valid_line_metric = True
        else:
            self.valid_line_metric = False

    def to_line_format_string(self, metrics_dict):
        if 'measurement' in metrics_dict:
            measurement = metrics_dict['measurement']
        else:
            return ''

        if 'tags' in metrics_dict:
            tags = metrics_dict['tags']
        else:
            return ''

        if 'value' in metrics_dict:
            value = metrics_dict['value']
        else:
            return ''

        return f'{measurement},{tags} {value}'

    def send_metric(self):
        if self.proto == "tcp":
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        elif self.proto == "udp":
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else:
            print("Must define protocol in Telegraf()")
            return

        if self.valid_line_metric:
            print(self.line_metric)
            addr_tupl = (self.server, int(self.port))
            sock.connect(addr_tupl)
            sock.send(str.encode(self.line_metric))
            sock.close()
        else:
            print("No metric defined, call Telegraf.metric(measurement, \
                  tags, values first!)")


# tag = {"host": "localhost", "interface": "wlan0"}
# value = {"wlan0_bytes_in": 125125, "wlan0_bytes_out": 9999}
# g = Telegraf(telegraf_server, telegraf_port, telegraf_proto)
# g.metric("testmeasurement", tag, value)

# print(g.metric)
# g.send_metric()
# print(g.resp)
