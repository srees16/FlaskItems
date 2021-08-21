from user import User
from werkzeug.security import safe_str_cmp

'''users = [
    {'name': 'bob',
     'id': 1,
     'password': 'asdf'
     }
    ]
'''

users = [User(1, 'bob', 'asdf')]

'''username_mapping = {'bob': {'name': 'bob',
     'id': 1,
     'password': 'asdf'
     }
    }
'''

username_mapping = {u.username: u for u in users}

'''userid_mapping = {1: {'name': 'bob',
     'id': 1,
     'password': 'asdf'
     }
    }
'''

userid_mapping = {u.id: u for u in users}


def authentication(username, password):
    user = username_mapping.get(username, None)
    if user and safe_str_cmp(user.password, password):
        return user
    return {'message': 'Invalid JWT token'}

def identify(payload):
    id = payload['identity']
    return userid_mapping.get(id, None)
        