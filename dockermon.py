#!/usr/bin/env python
"""docker monitor using docker /events HTTP streaming API"""

from contextlib import closing
from functools import partial
from socket import socket, AF_UNIX
from subprocess import Popen, PIPE
from sys import stdout, version_info
import json
import shlex

if version_info[:2] < (3, 0):
    from httplib import OK as HTTP_OK
else:
    from http.client import OK as HTTP_OK

__version__ = '0.1.0'
bufsize = 1024


class HTTPError(Exception):
    pass


def read_http_header(sock):
    """Read HTTP header from socket, return header and rest of data."""
    buf = []
    hdr_end = '\r\n\r\n'

    while True:
        buf.append(sock.recv(bufsize).decode('utf-8'))
        data = ''.join(buf)
        i = data.find(hdr_end)
        if i == -1:
            continue
        return data[:i], data[i + len(hdr_end):]


def header_status(header):
    """Parse HTTP status line, return status (int) and reason."""
    status_line = header[:header.find('\r')]
    # 'HTTP/1.1 200 OK' -> (200, 'OK')
    fields = status_line.split(None, 2)
    return int(fields[1]), fields[2]


def watch(callback, path='/var/run/docker.sock'):
    """Watch docker events. Will call callback with each new event (dict)."""
    sock = socket(AF_UNIX)
    sock.connect(path)

    with closing(sock):
        sock.sendall(b'GET /events HTTP/1.1\n\n')
        header, payload = read_http_header(sock)
        status, reason = header_status(header)
        if status != HTTP_OK:
            raise HTTPError('bad HTTP status: %s %s' % (status, reason))

        # Messages are \r\n<size in hex><JSON payload>\r\n
        buf = [payload]
        while True:
            buf.append(sock.recv(bufsize).decode('utf-8'))
            data = ''.join(buf)
            i = data.find('\r\n')
            if i == -1:
                continue

            size = int(data[:i], 16)
            start = i + 2  # Skip initial \r\n

            if len(data) < start + size + 2:
                continue
            payload = data[start:start+size]
            callback(json.loads(payload))
            buf = [data[start+size+2:]]  # Skip \r\n suffix


def print_callback(msg):
    """Print callback, prints message to stdout as JSON in one line."""
    json.dump(msg, stdout)
    stdout.write('\n')
    stdout.flush()


def prog_callback(prog, msg):
    """Program callback, calls prog with message in stdin"""
    pipe = Popen(prog, stdin=PIPE)
    data = json.dumps(msg)
    pipe.stdin.write(data.encode('utf-8'))
    pipe.stdin.close()


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--prog', default=None,
                        help='program to call (e.g. "jq --unbuffered .")')
    args = parser.parse_args()

    if args.prog:
        prog = shlex.split(args.prog)
        callback = partial(prog_callback, prog)
    else:
        callback = print_callback

    try:
        watch(callback)
    except (KeyboardInterrupt, EOFError):
        pass
