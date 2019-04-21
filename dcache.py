import diskcache
import pickle
import hashlib


r = diskcache.Cache('tmp')

class Cache:
    CACHED_SECONDS = 768
    
    @classmethod
    def get(cls, path):
        if cls.has(path):
            return pickle.loads(r.get(cls._get_key(path)))
        return False

    @classmethod
    def has(cls, path):
        return r.get(cls._get_key(path)) is not None

    @classmethod
    def set(cls, path, entity, expire=CACHED_SECONDS):
        return r.set(cls._get_key(path), pickle.dumps(entity), expire)

    @classmethod
    def rem(cls, path):
        return r.delete(cls._get_key(path))

    @staticmethod
    def _get_key(path):
        return 'onelist:' + hashlib.md5(path.encode()).hexdigest()
