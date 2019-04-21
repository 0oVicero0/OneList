import time
import schedule
import threading
from dcache import Cache
from config import config
from onedrive import OneDrive
from utils import path_format


od = OneDrive()


class Process:
    tasks = []

    @staticmethod
    def runner():
        while True:
            schedule.run_pending()
            time.sleep(1)

    @staticmethod
    def refresh_token():
        od.get_access()
        od.get_resource()
        od.get_access(od.resource_id)

    @classmethod
    def refresh_difference(cls):
        cls.tasks.append({'full_path': config.start_directory})

    @classmethod
    def worker(cls):
        while True:
            if len(cls.tasks) < 1:
                time.sleep(.1)
                continue

            c = cls.tasks.pop(0)
            info = od.list_items_with_cache(c['full_path'], True)

            for f in info.files:
                p = f['full_path']

                if not Cache.has(p):
                    continue

                file = Cache.get(p).files[0]
                if file['hash'] != f['hash']:
                    print('expired file: %s' % p)
                    Cache.rem(p)

            for f in info.folders:
                p = f['full_path']

                if not Cache.has(p):
                    print('no cached: %s' % p)
                    new = od.list_items_with_cache(p, True)

                    cls.cache_all(new)
                    cls.tasks += new.folders[1:]
                    continue

                folder = Cache.get(p).folders[0]
                if folder['hash'] != f['hash']:
                    print('expired folder: %s' % p)
                    new = od.list_items_with_cache(p, True)

                    cls.cache_all(new)
                    cls.tasks += new.folders[1:]

    @staticmethod
    def cache_all(info):
        for f in info.folders:
            Cache.set(f['full_path'], od.list_items_with_cache(
                f['full_path'], True), config.structure_cached_seconds)


Process.refresh_token()
Process.refresh_difference()

schedule.every(config.refresh_seconds).seconds.do(Process.refresh_token)
schedule.every(config.diff_seconds).seconds.do(Process.refresh_difference)

threading.Thread(target=Process.runner).start()
for _ in range(config.threads):
    threading.Thread(target=Process.worker).start()
