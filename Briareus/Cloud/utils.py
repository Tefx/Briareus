from gevent import monkey; monkey.patch_all()
from Corellia.client import Client
from Corellia.kvstore import KVStore
from ..config import config
from uuid import uuid1
import Husky
from gevent import sleep

class Cloud(object):
    def __init__(self, f):
        self.f = f
        self.put_client = Client(config.host, "Briareus", pickler=Husky, serialize=True, interval=0.01)
        self.get_client = Client(config.host, "Briareus", pickler=Husky, serialize=False)
        # self.client = Client(config.host, "Briareus", pickler=Husky, serialize=True, interval=0.01)

    def __call__(self, *args):
        key = self.put_client.put_task("eval", (self.f, args))
        return self.get_client.get_result(key, block=True)
        # return Client(config.host, "Briareus", pickler=Husky, serialize=False).eval(self.f, args)
        # return self.client.eval(self.f, args)

    def __getstate__(self):
        return Husky.dumps(self.f)

    def __setstate__(self, state):
        self.f = Husky.loads(state) 

kvstore = KVStore(config.host, "CachedData", serialize=True, interval=0.01)

class CachedData(object):
    def __init__(self, var):
        self.value = var
        self.put(self.value)

    def __getstate__(self):
        return self.id

    def __setstate__(self, state):
        self.id = state

    def __getattr__(self, name):
        if name == "value":
            self.__dict__["value"] = self.get(self.id)
            return self.__dict__["value"]
        else:
            return getattr(self.value, name)

    def put(self, value):
        self.id = uuid1().hex
        value = Husky.dumps(value)
        kvstore.set(self.id, value, serialize=True)

    def get(self, key):
        res = kvstore.get(key, serialize=False)
        while not res:
            sleep(0.01)
            res = kvstore.get(key, serialize=False)
        return Husky.loads(res)

    def __del__(self):
        pass