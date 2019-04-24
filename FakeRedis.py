#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# Author:  MoeClub.org

# Fake Redis, Cache in memory.
# Support type: bytes, int, str, list, dict

from threading import Thread
import base64
import pickle
import time


class Cache:
    def __init__(self, interval=1):
        self._interval_time = int(interval)
        self._cache = {}
        self._valid()

    def _time(self):
        return int(time.time())

    def _interval(self, interval=None):
        try:
            assert interval
            interval = int(interval)
        except:
            interval = self._interval_time
        time.sleep(interval)

    def get(self, item, obj='value'):
        try:
            assert isinstance(item, str)
            assert item and item in self._cache
            if obj == 'value':
                value = base64.b64decode(str(self._cache[item][obj]).encode('utf-8'))
                if not self._cache[item]['bytes']:
                    value = pickle.loads(value)
            else:
                value = self._cache[item][obj]
            return value
        except Exception as error:
            print(error)
            return None

    def exists(self, item):
        try:
            assert isinstance(item, str)
            assert item and item in self._cache
            return 1
        except:
            return 0

    def set(self, item, item_value, expire=7, refresh=True):
        try:
            if refresh and item in self._cache:
                self.delete(item)
            self._cache[item] = {}
            if not isinstance(item_value, bytes):
                self._cache[item]['bytes'] = 0
                item_value = pickle.dumps(item_value)
            else:
                self._cache[item]['bytes'] = 1
            self._cache[item]['value'] = base64.b64encode(item_value).decode('utf-8')
            self._cache[item]['ttl'] = str(9999999999) if expire == 0 else str(int(self._time()) + int(expire))
            return "OK"
        except Exception as error:
            print(error)
            return 0

    def delete(self, item):
        try:
            if isinstance(item, dict):
                for item_cache in item:
                    assert item_cache and item_cache in self._cache
                    self._cache.pop(item_cache)
            elif isinstance(item, str):
                assert item and item in self._cache
                self._cache.pop(item)
            else:
                raise Exception
        except:
            return False

    def flush(self):
        self._cache = {}

    def _ttl(self):
        while True:
            try:
                Now = self._time()
                for item in self._cache:
                    try:
                        if int(self._cache[item]['ttl']) - int(self._interval_time) < Now:
                            self.delete(item)
                    except:
                        break
                self._interval()
            except:
                continue

    def _valid(self):
        Task = Thread(target=self._ttl)
        Task.setDaemon(True)
        Task.start()


if __name__ == '__main__':
    c = Cache()
    c.set('item', 0)
    print(c.get('item'))


