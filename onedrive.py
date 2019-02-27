# Author:  MoeClub.org, sxyazi

from cache import Cache
from utils import path_format
from urllib import request, parse
import json
import requests


class OneDrive():
    _request_headers = {'User-Agent': 'ISV|MoeClub|OneList/1.0',
                        'Accept': 'application/json; odata.metadata=none'}

    class ItemInfo:
        def __init__(self):
            self.files = []
            self.folders = []

    def __init__(self):
        self.api_url = ''
        self.resource_id = ''

        self.expires_on = ''
        self.access_token = ''
        self.refresh_token = ''
        self._load_config()

    def get_access(self, resource='https://api.office.com/discovery/'):
        res = self._http_request('https://login.microsoftonline.com/common/oauth2/token', 'POST', {
            'client_id': 'ea2b36f6-b8ad-40be-bc0f-e5e4a4a7d4fa',
            'client_secret': 'h27zG8pr8BNsLU0JbBh5AOznNS5Of5Y540l/koc7048=',
            'redirect_uri': 'http://localhost/onedrive-login',
            'refresh_token': self.refresh_token,
            'grant_type': 'refresh_token',
            'resource': resource
        })

        self.expires_on = res['expires_on']
        self.access_token = res['access_token']
        self.refresh_token = res['refresh_token']

        if not self.access_token:
            print('Unauthorized')
            exit(1)

    def get_resource(self):
        res = self._http_request(
            'https://api.office.com/discovery/v2.0/me/services')

        for item in res['value']:
            if item['serviceApiVersion'] == 'v2.0':
                self.api_url = item['serviceEndpointUri']
                self.resource_id = item['serviceResourceId']

        if not self.api_url:
            raise Exception('Failed to get api url')

    def list_items(self, path='/'):
        url = '%s/drive/root:%s/?expand=children(select=name,size,file,folder,parentReference,lastModifiedDateTime)' % (
            self.api_url, parse.quote(path_format(path)))
        res = self._http_request(url)

        info = self.ItemInfo()
        self._append_item(info, res)

        if 'children' in res:
            for children in res['children']:
                self._append_item(info, children)

        return info

    def list_all_items(self, path='/'):
        ret = self.ItemInfo()
        tasks = [{'full_path': path}]

        while len(tasks) > 0:
            c = tasks.pop(0)

            tmp = self.list_items(c['full_path'])
            tasks += tmp.folders[1:]

            ret.files += tmp.files
            ret.folders += tmp.folders[1:]

        return ret

    def list_cached_items(self, path='/'):
        path = path_format(path)
        if not Cache.has(path):
            Cache.set(path, self.list_items(path))

        return Cache.get(path)

    def _load_config(self):
        try:
            conf = {}
            with open('config.json', 'r', encoding='utf-8') as f:
                conf = json.loads(f.read())

            if 'token' in conf:
                self.refresh_token = conf['token']
        except:
            pass

    def _http_request(self, url, method='GET', data={}, headers={}):
        if method == 'GET':
            fn = requests.get
        else:
            fn = requests.post

        if self.access_token:
            headers['Authorization'] = 'Bearer ' + self.access_token

        return fn(url, data=data, headers={**self._request_headers, **headers}).json()

    def _append_item(self, info, item):
        if 'path' not in item['parentReference']:
            path = item['name'] = '/'
        else:
            path = item['parentReference']['path'][12:] or '/'

        dic = {
            'name': item['name'],
            'size': item['size'],
            'folder': path,
            'full_path': path_format(path + '/' + item['name']),
            'updated_at': item['lastModifiedDateTime']
        }
        if '@content.downloadUrl' in item:
            dic['download_url'] = item['@content.downloadUrl']

        if 'file' in item:
            info.files.append(dic)
        else:
            info.folders.append(dic)
