# Author:  MoeClub.org, sxyazi

import redis
import pickle
import hashlib

r = redis.Redis(host='127.0.0.1', port=6379, db=0)
# r = redis.Redis(host='Redis_URL', port=PORT, db=0, password='Password', ssl=True, ssl_ca_certs='ca.pem')


class Cache:
    CACHED_SECONDS = 768

    @classmethod
    def get(cls, path):
        if cls.has(path):
            return pickle.loads(r.get(cls._get_key(path)))
        return False

    @classmethod
    def has(cls, path):
        return r.exists(cls._get_key(path))

    @classmethod
    def set(cls, path, entity, expire=CACHED_SECONDS):
        return r.set(cls._get_key(path), pickle.dumps(entity), expire)

    @classmethod
    def rem(cls, path):
        return r.delete(cls._get_key(path))

    @staticmethod
    def _get_key(path):
        return 'onelist:' + hashlib.md5(path.encode()).hexdigest()
