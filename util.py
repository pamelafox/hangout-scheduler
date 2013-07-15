import os
from dateutil.parser import parse


def get_host():
    port = os.environ['SERVER_PORT']
    host = os.environ['SERVER_NAME']
    if port and port != '80':
        host = '%s:%s' % (host, port)
    return 'http://' + host


def convert_htmldatetime(htmldatetime):
    return parse(htmldatetime)
