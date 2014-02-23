from wsgiref.validate import validator
from wsgiref.simple_server import make_server

from app import make_app

wsgi_app = make_app()

validator_app = validator(wsgi_app)

httpd = make_server('', 8000, validator_app)
print "Listening on port 8000...."
httpd.serve_forever()