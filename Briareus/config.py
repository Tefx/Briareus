import os


CONF_LOC = ["/etc/briareus.conf",
            os.path.join(os.path.expanduser("~"), ".briareus.conf"),
            "./briareus.conf"]

class Config(object):
    def __init__(self):
        self.configs = {}
        for f in CONF_LOC:
            if os.path.exists(f):
                self.parse(f)

    def parse(self, path):
        with open(path, "r") as f:
            self.configs.update(eval(f.read()))

    def __getattr__(self, name):
        return self.configs[name]

config = Config()


if __name__ == '__main__':
    print config.host