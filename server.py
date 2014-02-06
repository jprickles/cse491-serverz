#!/usr/bin/env python
import random
import socket
import time
import urlparse
import cgi
import jinja2
from StringIO import StringIO
from mimetools import Message

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

    if req == 'GET':
        if reqType == '/':
            handle_slash(conn, urlInfo, env)
        elif reqType == '/content':
            handle_content(conn, urlInfo, env)
        elif reqType == '/file':
            handle_file(conn, urlInfo, env)
        elif reqType == '/image':
            handle_image(conn, urlInfo, env)
        elif reqType == '/form':
            handle_form(conn, urlInfo, env)
        elif reqType == '/submit':
            handle_submit_get(conn, urlInfo, env)
        else:
            not_found(conn, urlInfo, env)
    elif req == 'POST':
        handle_post(conn, info, env)
    conn.close()

def handle_slash(conn, urlInfo, env):
    content = 'HTTP/1.0 200 OK\r\n' + \
              'Content-type: text/html\r\n' + \
              '\r\n'
    conn.send(content)

    template = env.get_template('index_page.html').render()
    conn.send(template)

def handle_content(conn, urlInfo, env):
    content = 'HTTP/1.0 200 OK\r\n' + \
              'Content-type: text/html\r\n' + \
              '\r\n'
    conn.send(content)
    template = env.get_template('content_page.html').render()
    conn.send(template)

def handle_file(conn, urlInfo, env):
    content = 'HTTP/1.0 200 OK\r\n' + \
              'Content-type: text/html\r\n' + \
              '\r\n'
    conn.send(content)

    template = env.get_template('files_page.html').render()
    conn.send(template)

def handle_image(conn, urlInfo, env):
    content = 'HTTP/1.0 200 OK\r\n' + \
              'Content-type: text/html\r\n' + \
              '\r\n'
    conn.send(content)

    template = env.get_template('image_page.html').render()
    conn.send(template)

def handle_form(conn, urlInfo, env):
    content = 'HTTP/1.0 200 OK\r\n' + \
              'Content-type: text/html\r\n' + \
              '\r\n'
    conn.send(content)

    template = env.get_template('form_page.html').render()
    conn.send(template)

def handle_submit_get(conn, urlInfo, env):
    content = 'HTTP/1.0 200 OK\r\n' + \
              'Content-type: text/html\r\n' + \
              '\r\n'
    conn.send(content)
    query = urlInfo.query
    data = urlparse.parse_qs(query)

    try:
        firstname = data['firstname'][0]
    except KeyError:
        firstname = ''
    try:
        lastname = data['lastname'][0]
    except KeyError:
        lastname = ''

    vars = dict(firstname=firstname, lastname=lastname)
    template = env.get_template('submit_get.html').render(vars)
    conn.send(template)

def handle_post(conn, info, env):
    content = 'HTTP/1.0 200 OK\r\n' + \
              'Content-type: text/html\r\n' + \
             '\r\n'
    conn.send(content)

    infoData = info.split()

    contentLength = 0;
    contentType = '';
    lineSplit = info.split('\r\n')
    for s in lineSplit:
        if 'Content-Type' in s:
            contentType = s.split()[1]
        if 'Content-Length' in s:
            contentLength = int (s.split()[1])

    # read characters
    for i in range(contentLength):
        content += conn.recv(1)

    if contentType == 'application/x-www-form-urlencoded':
        query = content.splitlines()[-1]
        data = urlparse.parse_qs(query)

        try:
            firstname = data['firstname'][0]
        except KeyError:
            firstname = ''
        try:
            lastname = data['lastname'][0]
        except KeyError:
            lastname = ''
        vars = dict(firstname=firstname, lastname=lastname)
        template = env.get_template('submit_post_application.html').render(vars)
        conn.send(template)

    elif contentType == 'multipart/form-data;':
        # contains request info as well as header info
        headers = info.split('\r\n', 1)[1]
        headers = headers[:-4]
        headers = headers.split('\r\n')
        d = {}
        for line in headers:
            k, v = line.split(': ', 1)
            d[k.lower()] = v
        environ = {}
        environ['REQUEST_METHOD'] = 'POST'
        form = cgi.FieldStorage(
            headers = d,
            fp=StringIO(content),
            environ=environ
        )
        firstname=''
        try:
            firstname = form['firstname'].value
        except KeyError:
            firstname = ''
        try:
            lastname = form['lastname'].value
        except KeyError:
            lastname = ''
        vars = dict(firstname=firstname, lastname=lastname)
        template = env.get_template('submit_post_application.html').render(vars)
        conn.send(template)

def not_found(conn, urlInfo, env):
    content = 'HTTP/1.0 404 Not Found\r\n' + \
              'Content-type: text/html\r\n' + \
              '\r\n'
    conn.send(content)

    template = env.get_template("not_found.html").render()
    conn.send(template)

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