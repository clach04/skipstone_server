#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
"""Emulate WDTV api enough to work with Pebble Skipstone
"""

import cgi
import json  # Python 2.6+
import mimetypes
import os
from pprint import pprint
import sys
from wsgiref.simple_server import make_server


def play_pause():
    print(sys._getframe().f_code.co_name)

def rewind():
    print(sys._getframe().f_code.co_name)

def forward():
    print(sys._getframe().f_code.co_name)


# See https://github.com/Skipstone/Skipstone/blob/master/src/js/src/wdtv.js
# for commands
commands = {
    'H': rewind,
    'I': forward,
    'p': play_pause,
}

def not_found(environ, start_response):
    """serves 404s."""
    #start_response('404 NOT FOUND', [('Content-Type', 'text/plain')])
    #return ['Not Found']
    start_response('404 NOT FOUND', [('Content-Type', 'text/html')])
    return ['''<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>404 Not Found</title>
</head><body>
<h1>Not Found</h1>
<p>The requested URL /??????? was not found on this server.</p>
</body></html>''']

# A relatively simple WSGI application. It's going to print out the
# environment dictionary after being updated by setup_testing_defaults
def simple_app(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/plain')]
    result = []

    path_info = environ['PATH_INFO']

    # Returns a dictionary in which the values are lists
    get_dict = cgi.parse_qs(environ['QUERY_STRING'])

    # POST values
    # the environment variable CONTENT_LENGTH may be empty or missing
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0
    # Read POST body
    request_body = environ['wsgi.input'].read(request_body_size)

    if path_info and path_info == '/cgi-bin/toServerValue.cgi':
        data = json.loads(request_body)
        command = data['remote']
        #command_function = commands.get(command)
        command_function = commands[command]
        command_result = command_function()
        if command_result is None:
            # no idea what should be returned however Skipstone doesn't check :-)
            result.append('')
        else:
            result.append(command_result)
    else:
        return not_found(environ, start_response)

    start_response(status, headers)

    return result


def doit():
    server_port = 8000
    server_port = 8080
    server_port = 8777

    httpd = make_server('', server_port, simple_app)
    print("Serving on port %d..." % server_port)
    httpd.serve_forever()


def main(argv=None):
    if argv is None:
        argv = sys.argv

    doit()

    return 0


if __name__ == "__main__":
    sys.exit(main())
