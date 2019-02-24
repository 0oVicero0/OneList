#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# Author:  MoeClub.org

from cache import Cache
from urllib import request, parse
import json

# Get refresh_token.
# https://login.microsoftonline.com/common/oauth2/authorize?response_type=code&client_id=ea2b36f6-b8ad-40be-bc0f-e5e4a4a7d4fa&redirect_uri=http://localhost/onedrive-login

class onedrive():
    def __init__(self):
        self.Header = {'User-Agent': 'ISV|MoeClub|OneList/1.0', 'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'application/json; odata.metadata=none'}
        self.refresh_token = ''
        self.expires = None
        self.api_url = None
        self.access = None
        self.src_id = None
        self.item_all = {}
        self.item_all_path = []

    def get_access(self, resource='https://api.office.com/discovery/'):
        api_auth_url = "https://login.microsoftonline.com/common/oauth2/token"
        access_dict = {
            'client_id': "ea2b36f6-b8ad-40be-bc0f-e5e4a4a7d4fa",
            'client_secret': "h27zG8pr8BNsLU0JbBh5AOznNS5Of5Y540l/koc7048=",
            'redirect_uri': "http://localhost/onedrive-login",
            'refresh_token': self.refresh_token,
            'grant_type': "refresh_token",
            'resource': resource
        }
        Data = parse.urlencode(access_dict).encode('utf-8')
        Header = self.Header
        try:
            req_context = request.urlopen(request.Request(str(api_auth_url), method='POST', headers=Header, data=Data)).read().decode('utf-8')
            req_dict = json.loads(req_context)
            self.expires = req_dict["expires_on"]
            self.access = req_dict["access_token"]
            self.refresh_token = req_dict["refresh_token"]
        except:
            self.expires = None
            self.access = None

    def get_src(self):
        self.get_access()
        self.check_access()
        try:
            URL = "https://api.office.com/discovery/v2.0/me/services"
            req_src_context = self.req_item(URL)
            req_src_context_dict = json.loads(req_src_context)
            for item in req_src_context_dict['value']:
                if item['serviceApiVersion'] == 'v2.0':
                    self.api_url = item['serviceEndpointUri']
                    self.src_id = item['serviceResourceId']
            if not self.api_url:
                raise Exception
        except:
            self.api_url = None
            self.src_id = None

    def check_access(self):
        if not self.access:
            print("Unauthorized")
            exit(1)

    def req_item(self, URL, Method='GET'):
        self.check_access()
        Header = self.Header
        Header['Authorization'] = "Bearer " + self.access
        return request.urlopen(request.Request(str(URL), headers=Header, method=Method)).read().decode('utf-8')

    def list_item(self, Header, item_path):
        item_url = self.api_url + '/drive/root:/' + parse.quote(str(item_path)) + '?expand=children(select=lastModifiedDateTime,size,name,folder,file)'
        return json.loads(request.urlopen(request.Request(str(item_url), headers=Header, method='GET')).read().decode('utf-8'))

    def list_items(self, Header, item_path=''):
        item_dict = self.list_item(Header, item_path)
        if 'folder' in item_dict:
            item_list = item_dict['children']
            for item_list_child in item_list:
                if 'folder' in item_list_child:
                    self.list_items(Header, item_path + '/' + item_list_child['name'])
                elif 'file' in item_list_child:
                    self.item_all_path.append(item_path + '/' + item_list_child['name'])
        elif '@content.downloadUrl' in item_dict:
            self.item_all_path.append(item_path)
            self.item_all[item_path] = {
                'name': item_dict['name'],
                'size': item_dict['size'],
                'time': item_dict['lastModifiedDateTime'],
                'url': item_dict['@content.downloadUrl'],
                'web': item_dict['webUrl'],
            }

    def cache_list(self, item_path=''):
        item_path = item_path.strip('/')
        if Cache.has(item_path):
            self.item_all, self.item_all_path = Cache.get(item_path)
            return

        self.get_src()
        self.get_access(self.src_id)
        self.check_access()
        Header = self.Header
        Header['Authorization'] = "Bearer " + self.access
        self.list_items(Header, item_path)
        for item in self.item_all_path:
            if item in self.item_all:
                continue
            self.list_items(Header, item)

        Cache.set(item_path, (self.item_all, self.item_all_path))

