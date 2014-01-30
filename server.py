#!/usr/bin/env python
import random
import socket
import time
import urlparse

# Handles the connection
def handle_connection(conn):
    info = conn.recv(1000)
    
    request = info.split(' ')
    urlRequest = request[1]
    urlInfo = urlparse.urlparse(urlRequest)
    urlPath = urlInfo.path
    
    if request[0] == 'GET':
        try:
            host = request[3].split('\r')
            host = host[0]
        except IndexError:
            host = '';
        
        if urlPath == '/':
            handle_index(conn, urlInfo)
        elif urlPath == '/content':
            handle_content(conn, urlInfo)
        elif urlPath == '/file':
            handle_file(conn, urlInfo)
        elif urlPath == '/image':
            handle_image(conn, urlInfo)
        elif urlPath == '/form':
            handle_form(conn, urlInfo)
        elif urlPath == '/submit':
            handle_submit(conn, urlInfo, info, 'GET')
        else:
            handle_no_page(conn, urlInfo)
    elif request[0] == 'POST':
        if urlPath == '/submit':
           handle_submit(conn, urlInfo, info, 'POST')
        else:
            handle_post(conn, info)
        
    conn.close()

def handle_index(conn, urlInfo):
    toSend = 'HTTP/1.0 200 OK\r\n' + \
             'Content-type: text/html\r\n\r\n' + \
             '<h1>Hello, world.</h1>' + \
             'This is JPrickles\'s web server.' + \
             '<ul>' + \
             '<li><a href="/content">Content</a></li>' + \
             '<li><a href="/file">Files</a></li>' + \
             '<li><a href="/image">Images</a></li>' + \
             '<li><a href="/form">Form</a></li>' + \
             '</ul>'
    conn.send(toSend)

def handle_content(conn, urlInfo):
    toSend = 'HTTP/1.0 200 OK\r\n' + \
             'Content-type: text/html\r\n\r\n' + \
             '<p>Content page requested</p>'
    conn.send(toSend)

def handle_file(conn, urlInfo):
    toSend = 'HTTP/1.0 200 OK\r\n' + \
             'Content-type: text/html\r\n\r\n' + \
             '<p>File page requested</p>'
    conn.send(toSend)

def handle_image(conn, urlInfo):
    toSend = 'HTTP/1.0 200 OK\r\n' + \
             'Content-type: text/html\r\n\r\n' + \
             '<p>Image page requested</p>'
    conn.send(toSend)

def handle_form(conn, urlInfo):
    forms = 'HTTP/1.0 200 OK\r\n' + \
            'Content-type: text/html\r\n' + \
            '\r\n' + \
            "<form action='/submit' method='GET'>" + \
            "First Name:<input type='text' name='firstName'>" + \
            "Last Name:<input type='text' name='lastName'>" + \
            "<input type='submit' value='Submit Get'>" + \
            "</form>\r\n" + \
            "<form action='/submit' method='POST'>" + \
            "First Name:<input type='text' name='firstName'>" + \
            "Last Name:<input type='text' name='lastName'>" + \
            "<input type='submit' value='Submit Post'>" + \
            "</form>\r\n"
    conn.send(forms)

def handle_submit(conn, urlInfo, info, reqType):
    if reqType == "GET":
        query = urlInfo.query
    elif reqType == "POST":
        query = info.splitlines()[-1]
        
    data = urlparse.parse_qs(query)
    firstName = data['firstName'][0]
    lastName = data['lastName'][0]
    greeting = 'Hello Mr. %s %s.' % (firstName,lastName)
    toSend = 'HTTP/1.0 200 OK\r\n' + \
             'Content-type: text/html\r\n\r\n' + \
             '<p>' + \
             greeting + \
             '</p>'
    conn.send(toSend)

def handle_no_page(conn, urlInfo):
    toSend = 'HTTP/1.0 200 OK\r\n' + \
             'Content-type: text/html\r\n\r\n' + \
             '<h2>Page Not Found!! :(</h2>'
    conn.send(toSend)

def handle_post(conn, info):
    toSend = 'HTTP/1.0 200 OK\r\n' + \
             'Content-type: text/html\r\n\r\n' + \
             '<h2>hello world</h2>'
    conn.send(toSend)

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
        handle_connection( c )

if __name__ == '__main__':
    main()

