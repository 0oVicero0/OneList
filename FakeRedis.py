#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# Author:  MoeClub.org

from threading import Thread
import base64
import time


class Cache:
    def __init__(self, interval=1):
        self.cache = {}
        self.interval = int(interval)
        self.valid()

    def get_time(self, interval=None, sleep_time=False):
        if sleep_time:
            try:
                assert interval
                interval = int(interval)
            except:
                interval = self.interval
            time.sleep(interval)
        return int(time.time())

    def get(self, item, obj='value'):
        try:
            assert isinstance(item, str)
            assert item and item in self.cache
            return base64.b64decode(str(self.cache[item][obj]).encode('utf-8'))
        except:
            return None

    def exists(self, item):
        try:
            assert isinstance(item, str)
            assert item and item in self.cache
            return 1
        except:
            return 0

    def set(self, item, item_value, expire, refresh=True):
        try:
            if refresh and item in self.cache:
                self.delete(item)
            self.cache[item] = {}
            self.cache[item]['value'] = base64.b64encode(item_value).decode('utf-8')
            self.cache[item]['time'] = str(int(self.get_time()) + int(expire))
            return "OK"
        except:
            return 0

    def delete(self, item):
        try:
            if isinstance(item, dict):
                for item_cache in item:
                    assert item_cache and item_cache in self.cache
                    self.cache.pop(item_cache)
            elif isinstance(item, str):
                assert item and item in self.cache
                self.cache.pop(item)
            else:
                raise Exception
        except:
            return False

    def flush(self):
        self.cache = {}

    def cache_ttl(self):
        while True:
            try:
                Time_Now = self.get_time(sleep_time=True)
                for item in self.cache:
                    try:
                        if int(self.cache[item]['time']) > Time_Now:
                            self.delete(item)
                    except:
                        continue
            except:
                continue

    def valid(self):
        Loop = Thread(target=self.cache_ttl)
        Loop.setDaemon(True)
        Loop.start()


if __name__ == '__main__':
    c = Cache()
    c.set('item', 'value', 32)
    print(c.cache)

