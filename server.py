#!/usr/bin/env python
import random
import socket
import time
import urlparse
import cgi
import jinja2
import quixote
from StringIO import StringIO
from app import make_app
from wsgiref.validate import validator
from wsgiref.simple_server import make_server

# from quixote.demo import create_publisher
# from quixote.demo.mini_demo import create_publisher
# from quixote.demo.altdemo import create_publisher
# 
# _the_app = None
# def make_app():
#     global _the_app
# 
#     if _the_app is None:
#         p = create_publisher()
#         _the_app = quixote.get_wsgi_app()
# 
#     return _the_app

def handle_connection(conn):
    loader = jinja2.FileSystemLoader('./templates')
    env = jinja2.Environment(loader=loader)

    info = conn.recv(1)

    # info is headers
    while info[-4:] != '\r\n\r\n':
        info += conn.recv(1)

    # req is either POST or GET
    req = info.split('\r\n')[0].split(' ')[0]

    # reqType is the path extracted
    reqType = info.split('\r\n')[0].split(' ')[1]
    urlInfo = urlparse.urlparse(reqType)
    reqType = urlInfo.path
    query = urlInfo.query

    content       = '';
    contentLength = 0;
    contentType   = '';
    wsgi_input    = '';
    lineSplit     = info.split('\r\n')
    if req == 'POST':
        for s in lineSplit:
            if 'Content-Type' in s:
                contentType = s.split(' ', 1)[1]
            if 'Content-Length' in s:
                contentLength = int (s.split()[1])
        for i in range(contentLength):
            content += conn.recv(1)
        wsgi_input = StringIO(content)

    environ = {}
    environ['REQUEST_METHOD'] = req
    environ['PATH_INFO']      = reqType
    environ['QUERY_STRING']   = query
    environ['CONTENT_TYPE']   = contentType
    environ['CONTENT_LENGTH'] = contentLength
    environ['wsgi.input']     = wsgi_input
    environ['SCRIPT_NAME']    = ''

    def start_response(status, response_headers):
        conn.send('HTTP/1.0')
        conn.send(status)
        conn.send('\r\n')
        for (k,v) in response_headers:
            conn.send(k)
            conn.send(v)
        conn.send('\r\n\r\n')

    wsgi_app = make_app()                             # WSGI Make Application
    validator_app = validator(wsgi_app)               # WSGI Validator
    
    output   = wsgi_app(environ, start_response)
    for line in output:
        conn.send(line)

    conn.close()

def main():

    s = socket.socket()         # Create a socket object
    host = socket.getfqdn() # Get local machine name
    port = random.randint(8000, 9999)
    s.bind((host, port))        # Bind to the port

    print 'Starting server on', host, port
    print 'The Web server URL for this would be http://%s:%d/' % (host, port)

    s.listen(5)                 # Now wait for client connection.

    print 'Entering infinite loop; hit CTRL-C to exit'
    while True:
        # Establish connection with client.
        c, (client_host, client_port) = s.accept()
        print 'Got connection from', client_host, client_port
        handle_connection(c)

if __name__ == "__main__":
    main()
