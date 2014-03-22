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

    server.handle_connection(conn, 0, "args")

    assert 'HTTP/1.0 200' in conn.sent
    assert 'JPrickles' in conn.sent, \
        'Got: %s' % (repr(conn.sent),)

def test_handle_connection_content():
    conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")

    server.handle_connection(conn, 0)

    assert 'HTTP/1.0200' in conn.sent and 'Content' in conn.sent, \
        'Got: %s' % (repr(conn.sent),)

def test_handle_connection_file():
    conn = FakeConnection("GET /file HTTP/1.0\r\n\r\n")

    server.handle_connection(conn, 0)

    assert 'HTTP/1.0200' in conn.sent and 'files' in conn.sent, \
        'Got: %s' % (repr(conn.sent),)

def test_handle_connection_image():
    conn = FakeConnection("GET /image HTTP/1.0\r\n\r\n")

    server.handle_connection(conn, 0)

    assert 'HTTP/1.0200' in conn.sent, \
        'Got: %s' % (repr(conn.sent),)

def test_handle_connection_post():
    conn = FakeConnection("POST /post HTTP/1.0\r\n" + \
        "Content-Length: 300\r\n"
        "Content-Type: application/x-www-form-urlencoded\r\n\r\n" + \
        "firstname=Joe&lastname=Mama")

    server.handle_connection(conn, 0)

    assert 'HTTP/1.0200' in conn.sent and 'Hello Mr.' in conn.sent, \
        'Got: %s' % (repr(conn.sent),)

def test_handle_connection_submit():
    conn = FakeConnection("GET /submit?firstname=Joe&lastname=Mama HTTP/1.0\r\n\r\n")

    server.handle_connection(conn, 0)

    assert 'HTTP/1.0200' in conn.sent

def test_handle_connection_post_multipart():
    conn = FakeConnection('POST /post HTTP/1.1\r\nHost: arctic.cse.msu.edu:9005\r\nConnection: keep-alive\r\nContent-Length: 246\r\nCache-Control: max-age=0\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\nOrigin: http://arctic.cse.msu.edu:9005\r\nUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36\r\nContent-Type: multipart/form-data; boundary=----WebKitFormBoundarylALrWqUulNpISokN\r\nReferer: http://arctic.cse.msu.edu:9005/form\r\nAccept-Encoding: gzip,deflate,sdch\r\nAccept-Language: en-US,en;q=0.8\r\n\r\n------WebKitFormBoundarylALrWqUulNpISokN\r\nContent-Disposition: form-data; name="firstname"\r\n\r\nEthan\r\n------WebKitFormBoundarylALrWqUulNpISokN\r\nContent-Disposition: form-data; name="lastname"\r\n\r\nEttema\r\n------WebKitFormBoundarylALrWqUulNpISokN--\r\n')

    server.handle_connection(conn, 0)

    assert 'HTTP/1.0200' in conn.sent and "Hello Mr." in conn.sent, \
        'Got: %s' % (repr(conn.sent),)

def test_handle_not_found():
    conn = FakeConnection("GET /404 HTTP/1.0\r\n\r\n")

    server.handle_connection(conn, 0)
    
    assert 'Someone messed up' in conn.sent
    