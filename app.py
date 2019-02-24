from onedrive import OneDrive
from flask import Flask, redirect, render_template

app = Flask(__name__)


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

        print(file_name)
        if '/' in file_name:
            dirs[file_name[:file_name.index('/')]] = v
        else:
            files[file_name] = v

    return render_template('list.html', path=path, dirs=dirs, files=files, format=format)


if __name__ == '__main__':
    app.run(debug=True)
