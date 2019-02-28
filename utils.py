import pickle
import hashlib
from datetime import datetime


def item_hash(d):
    return hashlib.md5(pickle.dumps(d)).hexdigest()


def path_format(path):
    while '//' in path:
        path = path.replace('//', '/')

    return '/' + path.strip('/')
