#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
"""Emulate WDTV api enough to work with Pebble Skipstone
"""

import cgi
try:
    from java.net import InetAddress
except ImportError:
    # Not Jython
    InetAddress = None
import json  # Python 2.6+
import logging
import mimetypes
import os
from pprint import pprint
import socket
import SocketServer
import struct
import sys
from wsgiref.simple_server import make_server, WSGIServer, WSGIRequestHandler


import pyautogui  # https://github.com/asweigart/pyautogui

log = logging.getLogger(__name__)
logging.basicConfig()
log.setLevel(level=logging.DEBUG)


version_tuple = (0, 0, 1)
version = version_string = '%d.%d.%d' % version_tuple


def send_single_keypress(key_name):
    print(key_name)
    pyautogui.press(key_name)


def send_multiple_keypresses(key_press_list):
    for key_tuple in key_press_list:
        print key_tuple
        pyautogui.hotkey(*key_tuple)


def send_presses(presses_to_send):
    if isinstance(presses_to_send, basestring):
        # assume single key name
        command_function = send_single_keypress
    else:
        # assume list of, key presses (list of tuples)
        command_function = send_multiple_keypresses
    result = command_function(presses_to_send)
    return result


# See https://github.com/Skipstone/Skipstone/blob/master/src/js/src/wdtv.js
# for commands
commands = {
    '[': 'prevtrack',
    ']': 'nexttrack',
    'H': [('ctrl', 'shift', 'b'), ('ctrl', 'left')],  # rewind - send two sets of controls, like chinavision cvsb-983 remote
    'I': [('ctrl', 'shift', 'f'), ('ctrl', 'right')],  # rewind - send two sets of controls, like chinavision cvsb-983 remote
    'M': 'volumemute',
    'p': 'playpause',
    't': 'stop',
    'n': 'enter',  # OK
    'T': 'browserback',
    'u': 'up',
    'd': 'down',
    'l': 'left',
    'r': 'right',
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
        presses_to_send = commands[command]
        command_result = send_presses(presses_to_send)
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


def determine_local_ipaddr():
    local_address = None

    # Most portable (for modern versions of Python)
    if hasattr(socket, 'gethostbyname_ex'):
        for ip in socket.gethostbyname_ex(socket.gethostname())[2]:
            if not ip.startswith('127.'):
                local_address = ip
                break
    # may be none still (nokia) http://www.skweezer.com/s.aspx/-/pypi~python~org/pypi/netifaces/0~4 http://www.skweezer.com/s.aspx?q=http://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib has alonger one

    if sys.platform.startswith('linux'):
        import fcntl

        def get_ip_address(ifname):
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            return socket.inet_ntoa(fcntl.ioctl(
                s.fileno(),
                0x8915,  # SIOCGIFADDR
                struct.pack('256s', ifname[:15])
            )[20:24])

        if not local_address:
            for devname in os.listdir('/sys/class/net/'):
                try:
                    ip = get_ip_address(devname)
                    if not ip.startswith('127.'):
                        local_address = ip
                        break
                except IOError:
                    pass

    # Jython / Java approach
    if not local_address and InetAddress:
        addr = InetAddress.getLocalHost()
        hostname = addr.getHostName()
        for ip_addr in InetAddress.getAllByName(hostname):
            if not ip_addr.isLoopbackAddress():
                local_address = ip_addr.getHostAddress()
                break

    if not local_address:
        # really? Oh well lets connect to a remote socket (Google DNS server)
        # and see what IP we use them
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 53))
        ip = s.getsockname()[0]
        s.close()
        if not ip.startswith('127.'):
            local_address = ip

    return local_address


def doit():
    # TODO yep, currently hard coded if ran standalone
    port = 8000
    port = 8080
    port = 8777

    httpd = make_server('', port, simple_app, server_class=MyWSGIServer, handler_class=MyWSGIRequestHandler)
    local_ip = determine_local_ipaddr()
    log.info('wdtv simulator %s', version)
    log.info('Starting server: %r', (local_ip, port))
    log.info('To stop, issue CTRL-C or (Windows) CTRL-Break')
    log.info('Configure in Skipstone on phone using address: %s:%d', local_ip, port)
    httpd.serve_forever()


def main(argv=None):
    if argv is None:
        argv = sys.argv

    doit()

    return 0


if __name__ == "__main__":
    sys.exit(main())
