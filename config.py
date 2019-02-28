import json


class Config:
    def __init__(self, opts={}):
        self._options = opts

    def __str__(self):
        return json.dumps(self._options, indent=2)

    def __getattr__(self, name):
        if name in self._options:
            if isinstance(self._options[name], dict):
                return Config(self._options[name])
            else:
                return self._options[name]

        return None


def _parse_config():
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            return json.loads(f.read())
    except:
        return {}


config = Config(_parse_config())
