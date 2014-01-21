#!/usr/bin/env python
import random
import socket
import time

def get( conn, path ):
    if path == '/':
        conn.send('HTTP/1.0 200 OK \r\n')
        conn.send('Content-type: text/html \r\n')
        conn.send('\r\n')
        conn.send('<h1>Hello, World!</h1> this is pricket4\'s Web server! <br>')
        conn.send('<a href="/content">  Content   </a><br>')
        conn.send('<a href="/file">     File      </a><br>')
        conn.send('<a href="/image">    Image     </a><br>')
        conn.send('Thank you for connecting. ')
        conn.send('Good bye!')       
    elif path == '/content':
        conn.send('HTTP/1.0 200 OK \r\n')
        conn.send('Content-type: text/html \r\n')
        conn.send('\r\n')
        conn.send('<h1>Content</h1><br>')
        conn.send('Thank you for connecting. ')
        conn.send('Good bye!') 
    elif path == '/file':
        conn.send('HTTP/1.0 200 OK \r\n')
        conn.send('Content-type: text/html \r\n')
        conn.send('\r\n')
        conn.send('<h1>File</h1><br>')
        conn.send('Thank you for connecting. ')
        conn.send('Good bye!') 
    elif path == '/image':
        conn.send('HTTP/1.0 200 OK \r\n')
        conn.send('Content-type: text/html \r\n')
        conn.send('\r\n')
        conn.send('<h1>Image</h1><br>')
        conn.send('Thank you for connecting. ')
        conn.send('Good bye!') 
    else:
        conn.send('HTTP/1.0 200 OK \r\n')
        conn.send('Content-type: text/html \r\n')
        conn.send('\r\n')
        conn.send('<h1>Page Not Found</h1><br>')
        conn.send('Thank you for connecting. ')
        conn.send('Good bye!')        

def post( conn ):
    conn.send('HTTP/1.0 200 OK \r\n\r\n')
    conn.send('Hello World!')

def handle_connection( conn ):
    recv = conn.recv(1000)
    check = (recv).split('\r\n')[0].split(' ')[0]
    if check == 'GET':
        try:
            path = recv.split('\r\n')[0].split(' ')[1]
            get( conn, path )
        except IndexError:
            get( conn, '/404' )
    elif check == 'POST':
        post( conn )

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
        handle_connection( c )

if __name__ == '__main__':
    main()

