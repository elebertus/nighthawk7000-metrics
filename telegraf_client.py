import socket


# TODO: General error handling. Need to figure out how we want the caller to do first.
class Telegraf:

    def __init__(self, server, port, proto):
        self.server = server
        self.port = port
        self.proto = proto
        self.line_metric = None
        self.valid_line_metric = None

    def metric(self, measurement, tags, values):

        tags = self.to_line_format_string(tags)
        values = self.to_line_format_string(values)

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

        self.line_metric = f'{measurement},{tags} {values}'
        self.valid_line_metric = True

    def to_line_format_string(self, dict_me):
        if isinstance(dict_me, dict):
            return self.dict_to_line_string(dict_me)
        elif isinstance(dict_me, int):
            return self.dict_to_line_string({str(dict_me): dict_me})
        elif isinstance(dict_me, str):
            return self.dict_to_line_string({dict_me: 0})
        else:
            return "null=null"

    def dict_to_line_string(self, d):
        return ','.join(['%s=%s' % (key, value) for (key, value) in d.items()])

    def send_metric(self):
        if self.proto == "tcp":
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        elif self.proto == "udp":
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else:
            print("Must define protocol in Telegraf()")
            return

        if self.valid_line_metric:
            addr_tupl = (self.server, int(self.port))
            sock.connect(addr_tupl)
            sock.send(str.encode(self.line_metric))
            sock.close()
        else:
            print("No metric defined, call Telegraf.metric(measurement, tags, values first!)")


""""
tag = {"host": "localhost", "interface": "wlan0"}
value = {"wlan0_bytes_in": 125125, "wlan0_bytes_out": 9999}
g = Telegraf(telegraf_server, telegraf_port, telegraf_proto)
g.metric("testmeasurement", tag, value)

print(g.metric)
g.send_metric()
print(g.resp)
"""
