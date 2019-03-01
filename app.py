#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# Author:  MoeClub.org, sxyazi

from process import od
from config import config
from flask import Flask, abort, redirect, render_template


app = Flask(__name__)


# Views
@app.route('/favicon.ico')
def favicon():
    return abort(404)


@app.route('/', defaults={'path': config.start_directory})
@app.route('/<path:path>')
def catch_all(path):
    info = od.list_items_with_cache(path)

    if info.files and not info.folders:  # download
        return redirect(info.files[0]['download_url'])

    return render_template('list.html', path=path, info=info)


# Filters
@app.template_filter('date_format')
def date_format(str, format='%Y/%m/%d %H:%M:%S'):
    from dateutil import tz
    from datetime import datetime

    dt = datetime.strptime(str, "%Y-%m-%dT%H:%M:%SZ")
    return dt.replace(tzinfo=tz.tzutc()).astimezone(tz.gettz('Asia/Shanghai')).strftime(format)


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
