import json
import dbm  # Used for easy database creation
from cgi import escape  # Used for URL data parsing
from models import Document
from utils import check_post_data
from user_utils import check_credentials


def get_doc(environ, start_response):
    """Get Document for a given doc_id
    (and user credentials - username and key)"""

    args = environ['app.url_args']
    if args:
        doc_id = escape(args[0])
        username = escape(args[1])
        key = escape(args[2])

        if check_credentials(username, key):
            doc_db = dbm.open('doc', 'c')
            if doc_id in doc_db.keys():
                start_response('200 OK',
                               [('Content-Type', 'application/json')])
                json_doc = {'doc_id': doc_id, 'doc_text': doc_db[doc_id]}
                return [json.dumps(json_doc)]
            else:
                json_doc = {'status': False,
                            'message': 'Document does not exist.'}
    else:
        json_doc = {'status': False, 'message': 'Missing data in request.'}

    start_response('400 BAD DATA', [('Content-Type', 'application/json')])
    return [json.dumps(json_doc)]


def create_doc(environ, start_response):
    """Create a Document with a given doc_id and doc_text
    (and user credentials - username and key)"""

    size = check_post_data(environ, start_response)
    if size:
        data = environ['wsgi.input'].read(size)
        data = json.loads(data)

        try:
            doc_id = data['doc_id']
            doc_text = data['doc_text']
            username = data['username']
            key = data['key']

            if check_credentials(username, key):
                doc = Document()

                start_response('200 OK',
                               [('Content-Type', 'application/json')])
                json_doc = doc.create(doc_id=doc_id, doc_text=doc_text)
                return [json.dumps(json_doc)]
            else:
                raise KeyError

        except KeyError:
            start_response('400 BAD DATA',
                           [('Content-Type', 'application/json')])
            json_doc = {'status': False,
                        'message': 'Missing data.'}
            return [json.dumps(json_doc)]

    else:
        start_response('400 BAD DATA', [('Content-Type', 'application/json')])
        json_doc = {'status': False,
                    'message': 'Missing data.'}
        return [json.dumps(json_doc)]
