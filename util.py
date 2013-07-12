import os
import datetime


def get_host():
    port = os.environ['SERVER_PORT']
    host = os.environ['SERVER_NAME']
    if port and port != '80':
        host = '%s:%s' % (host, port)
    return 'http://' + host


def convert_htmldatetime(htmldatetime):
    return datetime.datetime.strptime(htmldatetime, '%Y-%m-%dT%H:%M:%S.%fZ')
