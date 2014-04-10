#!/usr/bin/env python
import random
import socket
import time
import urlparse
import cgi
import jinja2
import quixote
import StringIO
import imageapp
import argparse
import PIL
from StringIO import StringIO
from app import make_app
from wsgiref.validate import validator
from wsgiref.simple_server import make_server
from quixote.demo.altdemo import create_publisher

def handle_connection(conn, port, wsgi_app):
    loader = jinja2.FileSystemLoader('./templates')
    env = jinja2.Environment(loader=loader)

    info = conn.recv(1)
	
    # info is headers
    while info[-4:] != '\r\n\r\n':
        info += conn.recv(1)

    reqc              = StringIO(info)
    reqc.readline()
    headers           = {}
    headers['cookie'] = ''
    while (True):
        temp = reqc.readline()
        if temp == "\r\n":
            break

        temp = temp.split("\r\n")[0].split(":", 1)
        headers[temp[0].lower()] = temp[1]

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
    environ['REQUEST_METHOD']    = req
    environ['PATH_INFO']         = reqType
    environ['QUERY_STRING']      = query
    environ['CONTENT_TYPE']      = contentType
    environ['CONTENT_LENGTH']    = contentLength
    environ['wsgi.input']        = wsgi_input
    environ['SCRIPT_NAME']       = ''
    environ['SERVER_NAME']       = socket.getfqdn()
    environ['SERVER_PORT']       = str(port)
    environ['wsgi.errors']       = StringIO('blah')
    environ['wsgi.multithread']  = ''
    environ['wsgi.multiprocess'] = ''
    environ['wsgi.run_once']     = ''
    environ['wsgi.version']      = (2,0)
    environ['wsgi.url_scheme']   = 'http'
    environ['HTTP_COOKIE']       = headers['cookie']

    def start_response(status, response_headers):
        conn.send('HTTP/1.0 ')
        conn.send(status)
        conn.send('\r\n')
        for (k,v) in response_headers:
            conn.send('%s: %s\r\n' % (k,v))
        conn.send('\r\n')

    validator_app = validator(wsgi_app)               # WSGI Validator

    result        = wsgi_app(environ, start_response)

    for line in result:
        conn.send(line)

    conn.close()

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument( '-A', '--runApp', help = 'Application to run (image/altdemo/myapp)' )
    parser.add_argument( '-p', '--portNumb', help = 'Specified port number', type=int )
    
    args = parser.parse_args()

    # Handle port input (if there)
    if args.portNumb:
        port = args.portNumb
    else:
        port = random.randint(8000, 9999)

	# Determine what app to create
    if args.runApp == 'myapp':
	    wsgi_app = make_app()
    elif args.runApp == 'image':
        imageapp.setup()
        p        = imageapp.create_publisher()
        wsgi_app = quixote.get_wsgi_app()
    elif args.runApp == 'altdemo':
    	p        = create_publisher()
    	wsgi_app = quixote.get_wsgi_app()
    elif args.runApp == 'quotes':
    	import quotes
    	wsgi_app = quotes.setup()
    elif args.runApp == 'chat':
    	import chat
    	wsgi_app = chat.setup()
    elif args.runApp == 'cookie':
    	import cookieapp
        wsgi_app = cookieapp.wsgi_app
    else:
		print 'Invalid Application...'
		return
    	
    s = socket.socket()         # Create a socket object
    host = socket.getfqdn()     # Get local machine name
    s.bind((host, port))        # Bind to the port

    print 'Starting server on', host, port
    print 'The Web server URL for this would be http://%s:%d/' % (host, port)

    s.listen(5)                 # Now wait for client connection.

    print 'Entering infinite loop; hit CTRL-C to exit'
    while True:
        # Establish connection with client.
        c, (client_host, client_port) = s.accept()
        print 'Got connection from', client_host, client_port
        try:
            handle_connection(c, port, wsgi_app)
        finally:
            imageapp.teardown()

if __name__ == "__main__":
    main()
