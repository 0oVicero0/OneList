#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# Author:  MoeClub.org

import redis
import pickle
import hashlib
r = redis.Redis(host='127.0.0.1', port=6379, db=0)

class Cache:
    CACHED_SECONDS = 3000

    @classmethod
    def get(cls, path):
        if cls.has(path):
            return pickle.loads(r.get(cls._get_key(path)))
        return False

    @classmethod
    def has(cls, path):
        return r.exists(cls._get_key(path))

    @classmethod
    def set(cls, path, entity):
        return r.set(cls._get_key(path), pickle.dumps(entity), cls.CACHED_SECONDS)

    @staticmethod
    def _get_key(path):
        return 'onelist:' + hashlib.md5(path.encode()).hexdigest()
