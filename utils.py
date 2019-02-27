def path_format(path):
    while '//' in path:
        path = path.replace('//', '/')

    return '/' + path.strip('/')
