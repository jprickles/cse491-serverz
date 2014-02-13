import server

class FakeConnection(object):
    """
    A fake connection class that mimics a real TCP socket for the purpose
    of testing socket I/O.
    """
    def __init__(self, to_recv):
        self.to_recv = to_recv
        self.sent = ""
        self.is_closed = False

    def recv(self, n):
        if n > len(self.to_recv):
            r = self.to_recv
            self.to_recv = ""
            return r
            
        r, self.to_recv = self.to_recv[:n], self.to_recv[n:]
        return r

    def send(self, s):
        self.sent += s

    def close(self):
        self.is_closed = True

# Test a basic GET call.

def test_handle_connection():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>Hello, world.</h1>' + \
                      'This is JPrickles\'s Web server.' + \
                      '\n<a href="/content">Content</a>\n' + \
                      '<a href="/file">Files</a>\n' + \
                      '<a href="/image">Images</a>\n'
    expected_return = 'HTTP/1.0200 OK \r\nContent-type: text/html\r\n\r\n<html>\n<head>\n    <title>Home</title>\n</head>\n<body>\n\n<h1>Hello, world.</h1>\nThis is JPrickles\'s Web server.\n<br>\n<a href="/content">Content</a>\n<a href="/file">Files</a>\n<a href="/image">Images</a>\n\n</body>\n</html>'
    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)
    """
    assert 'HTTP/1.0 200' in conn.sent and 'JPrickles' in conn.sent, \
        'Got: %s' % (repr(conn.sent),)
    """

def test_handle_connection_content():
    conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h2>content</h2>'
    server.handle_connection(conn)
    expected_return = 'HTTP/1.0200 OK \r\nContent-type: text/html\r\n\r\n<html>\n<head>\n    <title>Content</title>\n</head>\n<body>\n\n<h2>content</h2>\n\n</body>\n</html>'

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)
    """
    assert 'HTTP/1.0 200' in conn.sent and 'content' in conn.sent, \
        'Got: %s' % (repr(conn.sent),)
    """

def test_handle_connection_file():
    conn = FakeConnection("GET /file HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h2>files</h2>'
    server.handle_connection(conn)
    expected_return = 'HTTP/1.0200 OK \r\nContent-type: text/html\r\n\r\n<html>\n<head>\n    <title>File</title>\n</head>\n<body>\n\n<h2>files</h2>\n\n</body>\n</html>'

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)
    """
    assert 'HTTP/1.0 200' in conn.sent and 'files' in conn.sent, \
        'Got: %s' % (repr(conn.sent),)
    """

def test_handle_connection_image():
    conn = FakeConnection("GET /image HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h2>images</h2>'
    server.handle_connection(conn)
    expected_return = 'HTTP/1.0200 OK \r\nContent-type: text/html\r\n\r\n<html>\n<head>\n    <title>Image</title>\n</head>\n<body>\n\n<h2>images</h2>\n\n</body>\n</html>'
    assert conn.sent.startswith(expected_return), 'Got: %s' % (repr(conn.sent),)
    """
    assert 'HTTP/1.0 200' in conn.sent and 'images' in conn.sent, \
        'Got: %s' % (repr(conn.sent),)
    """

def test_handle_connection_post():
    conn = FakeConnection("POST /post HTTP/1.0\r\n" + \
        "Content-Length: 300\r\n"
        "Content-Type: application/x-www-form-urlencoded\r\n\r\n" + \
        "firstname=Joe&lastname=Mama")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h3>hello world, submitted via post</h3>' + \
                      'Hello Mr. Joe Mama.'
    server.handle_connection(conn)

    expected_return = 'HTTP/1.0200 OK \r\nContent-type: text/html\r\n\r\n<html>\n<head>\n    <title>Post</title>\n</head>\n<body>\n\n<h3>hello world, submitted via post</h3>\nHello Mr. Joe Mama.\n\n</body>\n</html>'
    assert conn.sent.startswith(expected_return), 'Got: %s' % (repr(conn.sent),)
    """
    assert 'HTTP/1.0 200' in conn.sent and 'Hello Mr.' in conn.sent, \
        'Got: %s' % (repr(conn.sent),)
    """

def test_handle_connection_submit():
    conn = FakeConnection("GET /submit?firstname=Joe&lastname=Mama HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      'Hello Mr. Joe Mama.'
    server.handle_connection(conn)
    expected_return = 'HTTP/1.0200 OK \r\nContent-type: text/html\r\n\r\n<html>\n<head>\n    <title>Get</title>\n</head>\n<body>\n\nHello Mr. Joe Mama.\n\n</body>\n</html>'
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_post_multipart():
    conn = FakeConnection('POST /post HTTP/1.1\r\nHost: arctic.cse.msu.edu:9005\r\nConnection: keep-alive\r\nContent-Length: 246\r\nCache-Control: max-age=0\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\nOrigin: http://arctic.cse.msu.edu:9005\r\nUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36\r\nContent-Type: multipart/form-data; boundary=----WebKitFormBoundarylALrWqUulNpISokN\r\nReferer: http://arctic.cse.msu.edu:9005/form\r\nAccept-Encoding: gzip,deflate,sdch\r\nAccept-Language: en-US,en;q=0.8\r\n\r\n------WebKitFormBoundarylALrWqUulNpISokN\r\nContent-Disposition: form-data; name="firstname"\r\n\r\nEthan\r\n------WebKitFormBoundarylALrWqUulNpISokN\r\nContent-Disposition: form-data; name="lastname"\r\n\r\nEttema\r\n------WebKitFormBoundarylALrWqUulNpISokN--\r\n')

    server.handle_connection(conn)
    expected_return = 'HTTP/1.0200 OK \r\nContent-type: text/html\r\n\r\n<html>\n<head>\n    <title>Post</title>\n</head>\n<body>\n\n<h3>hello world, submitted via post</h3>\nHello Mr. Ethan Ettema.\n\n</body>\n</html>'

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)
    """
    assert 'HTTP/1.0 200' in conn.sent and "Hello Mr." in conn.sent, \
        'Got: %s' % (repr(conn.sent),)
    """

def test_handle_not_found():
    conn = FakeConnection("GET /404 HTTP/1.0\r\n\r\n")
    expected_return = "HTTP/1.0404 Not Found\r\nContent-type: text/html\r\n\r\n<html>\n<head>\n    <title>404</title>\n</head>\n<body>\n\n<h1>Someone messed up, page not found, sorry brah</h1>\n\n</body>\n</html>"

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)