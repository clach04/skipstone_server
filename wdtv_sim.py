#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
"""Emulate WDTV api enough to work with Pebble Skipstone
"""

import cgi
import json  # Python 2.6+
import logging
import mimetypes
import os
from pprint import pprint
import SocketServer
import sys
from wsgiref.simple_server import make_server, WSGIServer, WSGIRequestHandler

import pyautogui  # https://github.com/asweigart/pyautogui

log = logging.getLogger(__name__)
logging.basicConfig()
log.setLevel(level=logging.DEBUG)


def mute_toggle():
    key_name = 'volumemute'
    print(key_name)
    pyautogui.press(key_name)

def play_pause():
    key_name = 'playpause'
    print(key_name)
    pyautogui.press(key_name)

def stop():
    key_name = 'stop'
    print(key_name)
    pyautogui.press(key_name)

def enter():
    key_name = 'enter'
    print(key_name)
    pyautogui.press(key_name)

def back():
    key_name = 'backspace'
    print(key_name)
    pyautogui.press(key_name)

def next_track():
    key_name = 'nexttrack'
    print(key_name)
    pyautogui.press(key_name)

def previous_track():
    key_name = 'prevtrack'
    print(key_name)
    pyautogui.press(key_name)

def rewind():
    key_name = 'rewind'
    print(key_name)
    # send two sets of controls, like chinavision cvsb-983 remote
    pyautogui.hotkey('ctrl', 'shift', 'b')
    pyautogui.hotkey('ctrl', 'left')

def forward():
    key_name = 'forward'
    print(key_name)
    # send two sets of controls, like chinavision cvsb-983 remote
    pyautogui.hotkey('ctrl', 'shift', 'f')
    pyautogui.hotkey('ctrl', 'right')


# See https://github.com/Skipstone/Skipstone/blob/master/src/js/src/wdtv.js
# for commands
commands = {
    '[': previous_track,
    ']': next_track,
    'H': rewind,
    'I': forward,
    'M': mute_toggle,
    'p': play_pause,
    't': stop,
    'n': enter,  # OK
    'T': back,  # backspace
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


class MyWSGIRequestHandler(WSGIRequestHandler):
    """Do not perform Fully Qualified Domain Lookup.
    One networks with missing (or poor) DNS, getfqdn can take over 5 secs
    EACH network IO"""

    def address_string(self):
        """Return the client address formatted for logging.

        This version looks up the full hostname using gethostbyaddr(),
        and tries to find a name that contains at least one dot.

        """

        host, port = self.client_address[:2]
        return host  # socket.getfqdn(host)


class MyWSGIServer(WSGIServer):
    """Avoid default Python socket server oddities.
    
     1) Do not perform Fully Qualified Domain Lookup.
        On networks with missing (or poor) DNS, getfqdn() can take over
        5 secs EACH network IO.
     2) Do not allow address re-use.
        On machines where something is already listening on the requested
        port the default Windows socket setting for Python SocketServers
        is to allow the bind to succeed (even though it can't then service
        any requests).
        One possible workaround for Windows is to set the
        DisableAddressSharing registry entry:
        (HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\services\Afd\Parameters)
        and reboot. This registry setting prevents multiple sockets from binding
        to the same port and is essentially enabling SO_EXCLUSIVEADDRUSE on
        all sockets. See Java bug 6421091.
    """
    
    allow_reuse_address = False  # Use SO_EXCLUSIVEADDRUSE,  True only makes sense for testing
    
    def server_bind(self):
        """Override server_bind to store the server name."""
        SocketServer.TCPServer.server_bind(self)
        host, port = self.socket.getsockname()[:2]
        self.server_name = host  # socket.getfqdn(host)  i.e. use as-is do *not* perform reverse lookup
        self.server_port = port
        self.setup_environ()


def doit():
    # TODO yep, currently hard coded if ran standalone
    server_port = 8000
    server_port = 8080
    server_port = 8777

    httpd = make_server('', server_port, simple_app, server_class=MyWSGIServer, handler_class=MyWSGIRequestHandler)
    print("Serving on port %d..." % server_port)
    httpd.serve_forever()


def main(argv=None):
    if argv is None:
        argv = sys.argv

    doit()

    return 0


if __name__ == "__main__":
    sys.exit(main())
