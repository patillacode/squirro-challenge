import re               # Used for matching URLs
import json             # Used for json data formatting
from user_utils import get_user, create_user
from document_utils import get_doc, create_doc


def index(environ, start_response):
    """This function will be mounted on '/' """
    start_response('200 OK', [('Content-Type', 'text/html')])
    # return ['''Hello, looking for the API? \r\n Hello''']
    return [open('html/index.html').read()]

# map urls to functions
urls = [
    (r'^$', index),
    (r'user/(.+)$', get_user),
    (r'user/?$', create_user),
    (r'doc/(.+)?/(.+)?/(.+)?$', get_doc),
    (r'doc/?$', create_doc),
]


def app(environ, start_response):
    # We search for any matches with our available urls
    # if url is wrong we return a 404
    path = environ.get('PATH_INFO', '').lstrip('/')
    for regex, callback in urls:
        match = re.search(regex, path)
        if match is not None:
            environ['app.url_args'] = match.groups()
            return callback(environ, start_response)
    start_response('404 NOT FOUND', [('Content-Type', 'application/json')])
    return [json.dumps({'status': '404', 'message': '404 Not Found'})]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, app)
    srv.serve_forever()
