import time
import schedule
import threading
from cache import Cache
from onedrive import OneDrive
from utils import path_format


od = OneDrive()

od.get_access()
od.get_resource()
od.get_access(od.resource_id)


class Process:
    @classmethod
    def runner(cls):
        while True:
            schedule.run_pending()
            time.sleep(1)

    @classmethod
    def refreshes(cls):
        tasks = [{'full_path': '/'}]

        while len(tasks) > 0:
            c = tasks.pop(0)
            info = od.list_items_with_cache(c['full_path'], True)

            for f in info.folders:
                p = f['full_path']

                if not Cache.has(p):
                    print('no cached: %s' % p)
                    new = od.list_items_with_cache(p, True)

                    cls.cache_all(new)
                    tasks += new.folders[1:]
                    continue

                folder = Cache.get(p).folders[0]
                if folder['hash'] != f['hash']:
                    print('expired cache: %s' % p)
                    new = od.list_items_with_cache(p, True)

                    cls.cache_all(new)
                    tasks += new.folders[1:]

    @classmethod
    def cache_all(cls, info):
        for f in info.folders:
            Cache.set(f['full_path'], od.list_items_with_cache(
                f['full_path'], True))


threading.Thread(target=Process.runner).start()
schedule.every(5).minutes.do(Process.refreshes)
