#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# Author:  MoeClub.org, sxyazi

from process import od
from config import config
from utils import path_format
from flask import Flask, abort, redirect, render_template, Blueprint

bp = Blueprint('main', __name__, url_prefix=config.location_path)


# Views
@bp.route('/favicon.ico')
def favicon():
    return abort(404)


@bp.route('/', defaults={'path': '/'})
@bp.route('/<path:path>')
def catch_all(path):
    info = od.list_items_with_cache(
        path_format(config.start_directory + '/' + str(path)))

    if info.is_file:  # download
        return redirect(info.files[0]['download_url'])

    return render_template('list.html', info=info, path=path_format(path).strip('/'))


# Filters
@bp.app_template_filter('date_format')
def date_format(str, format='%Y/%m/%d %H:%M:%S'):
    from dateutil import tz
    from datetime import datetime

    dt = datetime.strptime(str, "%Y-%m-%dT%H:%M:%SZ")
    return dt.replace(tzinfo=tz.tzutc()).astimezone(tz.gettz('Asia/Shanghai')).strftime(format)


@bp.app_template_filter('file_size')
def file_size(size):
    unit = (
        ('B', 2**0),
        ('KB', 2**10),
        ('MB', 2**20),
        ('GB', 2**30),
        ('TB', 2**40),
        ('PB', 2**50),
        ('EB', 2**60),
        ('ZB', 2**70),
        ('YB', 2**80)
    )

    for k, v in unit:
        if size <= v * 1024:
            return '%s %s' % (round(size/v, 2), k)
    return 'unknown'


app = Flask(__name__)
app.register_blueprint(bp)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port='5000', debug=True)
