#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# Author:  MoeClub.org, sxyazi

from onedrive import OneDrive
from flask import Flask, redirect, render_template
from datetime import datetime
from dateutil import tz

app = Flask(__name__)


# Views
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    one = OneDrive()
    one.cache_list(path)

    # file
    if (len(one.item_all) == 1 and list(one.item_all)[0] == path):
        return redirect(one.item_all[path]['url'])

    # dir
    dirs, files = {}, {}
    for k, v in one.item_all.items():
        file_name = k

        if file_name[:len(path)] == path:
            file_name = file_name[len(path):]
        file_name = file_name.strip('/')

        if '/' in file_name:
            dirs[file_name[:file_name.index('/')]] = v
        else:
            files[file_name] = v

    return render_template('list.html', path=path, dirs=dirs, files=files)


# Filters
@app.template_filter('date_format')
def date_format(str, format='%Y/%m/%d %H:%M:%S'):
    return datetime.strptime(str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=tz.tzutc()).astimezone(tz.gettz('Asia/Shanghai')).strftime(format)


@app.template_filter('file_size')
def file_size(size):
    unit = {
        'B': 2**0,
        'KB': 2**10,
        'MB': 2**20,
        'GB': 2**30,
        'TB': 2**40,
        'PB': 2**50,
        'EB': 2**60,
        'ZB': 2**70,
        'YB': 2**80,
    }

    for k, v in unit.items():
        if size <= v * 1024:
            return '%s %s' % (round(size/v, 2), k)
    return 'unknown'


if __name__ == '__main__':
    app.run(debug=True)
