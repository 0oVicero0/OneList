import pickle
import hashlib
from datetime import datetime


def path_format(path):
    while '//' in path:
        path = path.replace('//', '/')

    return '/' + path.strip('/')
