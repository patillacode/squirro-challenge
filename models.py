import dbm


class User:

    def __init__(self):
        pass

    def create(self, username, key):
        try:
            user_db = dbm.open('user', 'c')
            # Check if user exists
            if username in user_db:
                return {'status': False, 'message': 'User already exists'}
            # Check if key is duplicated
            else:
                all_keys = []
                for k in user_db.keys():
                    all_keys.append(user_db[k])

                if key in all_keys:
                    return {'status': False, 'message': 'Key already exists'}
            # If user doesn't exist and key isn't duplicated
            # we create the new user with the given username and key
            user_db[username] = key
            return {'status': True, 'message': 'User created successfully'}
        finally:
            user_db.close()


class Document:

    def __init__(self):
        pass

    def create(self, doc_id, doc_text):
        try:
            doc_db = dbm.open('doc', 'c')
            # Check if document exists
            if doc_id in doc_db:
                return {'status': False, 'message': 'Document already exists'}
            # Create document
            # Note: duplicated text can happen. (not required to avoid this)
            doc_db[doc_id] = doc_text
            return {'status': True, 'message': 'Document created successfully'}
        finally:
            doc_db.close()
