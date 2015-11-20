import json
import dbm  # Used for easy database creation
from cgi import escape  # Used for URL data parsin
from models import User
from utils import check_post_data


def check_credentials(user, key):
    """Check if user matches with a given key"""

    user_db = dbm.open('user', 'c')
    if user in user_db.keys() and user_db[user] == key:
        return True
    return False


def get_user(environ, start_response):
    """Get user for a given username"""

    args = environ['app.url_args']
    if args:
        username = escape(args[0])
    else:
        username = 'None'

    user_db = dbm.open('user', 'c')
    if username in user_db.keys():
        start_response('200 OK', [('Content-Type', 'application/json')])
        json_doc = {'status': True,
                    'username': username,
                    'key': user_db[username]}
        return [json.dumps(json_doc)]

    start_response('400 BAD DATA', [('Content-Type', 'application/json')])
    json_doc = {'status': False,
                'message': 'User {0} does not exist.'.format(username)}
    return [json.dumps(json_doc)]


def create_user(environ, start_response):
    """Create a user with a given username and key"""

    size = check_post_data(environ, start_response)
    if size:
        data = environ['wsgi.input'].read(size)
        data = json.loads(data)

        username = data['username']
        key = data['key']
        user = User()

        start_response('200 OK', [('Content-Type', 'application/json')])
        json_doc = user.create(username=username, key=key)
        return [json.dumps(json_doc)]

    else:
        start_response('400 BAD DATA', [('Content-Type', 'application/json')])
        json_doc = {'status': False,
                    'message': 'Missing data.'}
        return [json.dumps(json_doc)]
