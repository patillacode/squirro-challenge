import re
import json


def index(environ, start_response):
    """This function will be mounted on "/" """
    start_response('200 OK', [('Content-Type', 'text/html')])
    return ['''Hello, looking for the API, try /api/''']


def not_found(environ, start_response):
    """Called if no URL matches."""
    start_response('404 NOT FOUND', [('Content-Type', 'text/plain')])
    return ['ERROR 404 - Not Found']


def api(environ, start_response):
    # the environment variable CONTENT_LENGTH may be empty or missing
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0

    if not request_body_size:
        return not_found(environ, start_response)

    data = environ['wsgi.input'].read(request_body_size)
    data = json.loads(data)

    # start_response('200 OK', [('Content-Type', 'text/html')])
    start_response('200 OK', [('Content-Type', 'application/json"')])
    return [json.dumps({'status': '200', 'data': data})]

# map urls to functions
urls = [
    (r'^$', index),
    (r'api/?$', api),
]


def application(environ, start_response):
    # We search for any matches with our available urls
    # if url is wrong we return a 404
    path = environ.get('PATH_INFO', '').lstrip('/')
    for regex, callback in urls:
        match = re.search(regex, path)
        if match is not None:
            environ['api.url_args'] = match.groups()
            return callback(environ, start_response)
    return not_found(environ, start_response)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
