# from http://docs.python.org/2/library/wsgiref.html

from wsgiref.util import setup_testing_defaults
import jinja2
import urlparse
import cgi

# A relatively simple WSGI application. It's going to print out the
# environment dictionary after being updated by setup_testing_defaults


class my_app:

    def __init__(self):
        loader      = jinja2.FileSystemLoader('./templates')
        self.env    = jinja2.Environment(loader=loader)
        self.output = []

    def start_app(self, environ, start_response):
        req           = environ['REQUEST_METHOD']
        path          = environ['PATH_INFO']
        query         = environ['QUERY_STRING']
        contentType   = environ['CONTENT_TYPE']
        contentLength = environ['CONTENT_LENGTH']
        wsgiInput     = environ['wsgi.input']

#        setup_testing_defaults(environ)

        status = '200 OK '
# CHANGED
        headers = [('Content-type: ', 'text/html')]

        if req == 'GET':
            if path == '/':
                self.handle_slash()
            elif path == '/content':
                self.handle_content()
            elif path == '/file':
                self.handle_file()
            elif path == '/image':
                self.handle_image()
                headers = [('Content-type: ', 'image/jpeg')]
            elif path == '/form':
                self.handle_form()
            elif path == '/submit':
                self.handle_submit_get(query)
            else:
                status = '404 Not Found'
                self.not_found()
        elif req == 'POST':
            self.handle_post(contentLength, contentType, wsgiInput, environ)

        start_response(status, headers)

        """
        ret = ["%s: %s\n" % (key, value)
               for key, value in environ.iteritems()]
        ret.insert(0, "This is your environ.  Hello, world!\n\n")
        """

#        return ret
        return self.output

    def handle_slash(self):
        vars = dict(title='Home')
        content = self.env.get_template('index_page.html').render(vars).encode('latin-1', 'replace')
        self.output.append(content)

    def handle_content(self):
        vars = dict(title='Content')
        content = self.env.get_template('content_page.html').render(vars).encode('latin-1', 'replace')
        self.output.append(content)

    def handle_file(self):
        vars = dict(title='File')
        content = self.env.get_template('files_page.html').render(vars).encode('latin-1', 'replace')
        self.output.append(content)
        self.serve_file()

    def serve_file(self):
        filename = 'file.txt'
        fp = open(filename, "rb")
        data = fp.read()
        fp.close()
        self.output.append(data)

    def handle_image(self):
        vars = dict(title='Image')
        content = self.env.get_template('image_page.html').render(vars).encode('latin-1', 'replace')
        # self.output.append(content)
        self.serve_image()

    def serve_image(self):
        filename = 'blake.jpg'
        fp = open(filename, "rb")
        data = fp.read()
        fp.close()
        self.output.append(data)

    def handle_form(self):
        vars = dict(title='Form')
        content = self.env.get_template('form_page.html').render(vars).encode('latin-1', 'replace')
        self.output.append(content)

    def send_200():
        return self.output.append['HTTP1.0 200 OK \r\n']

    def handle_submit_get(self, query):
        data = urlparse.parse_qs(query)

        try:
            firstname = data['firstname'][0]
        except KeyError:
            firstname = ''
        try:
            lastname = data['lastname'][0]
        except KeyError:
            lastname = ''

        vars = dict(firstname=firstname, lastname=lastname, title='Get')
        template = self.env.get_template('submit_get.html').render(vars).encode('latin-1', 'replace')
        self.output.append(template)

    def not_found(self):
        vars=dict(title='404')
        template = self.env.get_template('not_found.html').render(vars).encode('latin-1', 'replace')
        self.output.append(template)

    def handle_post(self, contentLength, contentType, wsgiInput, environ):
        d = []
        cgiCType = 'Content-Length: ' + str(contentLength)
        cgiCLength = 'Content-Type: ' + contentType
        d.append(cgiCType)
        d.append(cgiCLength)
        # contains request info as well as header info
        dic = {}
        if 'multipart' in contentType:
            for line in d:
                k, v = line.split(': ', 1)
                dic[k.lower()] = v

        form = cgi.FieldStorage(
            headers = dic,
            fp=wsgiInput,
            environ=environ
        )
        try:
            firstname = form['firstname'].value
        except KeyError:
            firstname = ''
        try:
            lastname = form['lastname'].value
        except KeyError:
            lastname = ''
        vars = dict(firstname=firstname, lastname=lastname, title='Post')
        template = self.env.get_template('submit_post_application.html').render(vars).encode('latin-1', 'replace')
        self.output.append(template)

def make_app():
    app = my_app()
    return app.start_app
