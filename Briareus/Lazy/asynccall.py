from gevent import monkey;monkey.patch_all()
import gevent
import inspect

class LazyDict(dict):
    def __init__(self, *args):
        super(LazyDict, self).__init__(*args)
        self.var_path = {}
        self.result_cache = {}

    def __getitem__(self, key):
        _result = super(LazyDict, self).__getitem__(key)
        if isinstance(_result, AsyncResult):
            _result = _result._result
            self.__setitem__(key, _result)
        return _result

class AsyncResult(object):
    next_id = 0
    def __init__(self, greenlet, r_vars=[], w_vars=[]):
        self.greenlet = greenlet
        self.r_vars = r_vars
        self.w_vars = w_vars
        self.__class__.next_id += 1
        self.uid = self.__class__.next_id

    def __getattr__(self, name):
        if name == "_result":
            self.greenlet.join()
            self.__dict__["_result"] = self.greenlet.value
            return self.__dict__["_result"]
        else:
            return getattr(self._result, name)


# class AsyncCallable(object):
#     def __init__(self, f):
#         self.f = f

#     def __call__(self, *args, **kargs):
#         greenlet = gevent.spawn(self.f, *args, **kargs)
#         return AsyncResult(greenlet)

import types

def AsyncCallable(r_vars, w_vars):
    def callWithVars(f):
        def func(*args, **kargs):
            greenlet = gevent.spawn(f, *args, **kargs)
            return AsyncResult(greenlet, r_vars, w_vars)
        return func
    return callWithVars


from uuid import uuid1

class AsyncFunction(object):
    def __init__(self, f):
        self.uuid = "%s.%s" % (uuid1().hex, f.func_name)
        self.func = types.FunctionType(f.func_code, 
                                       f.func_globals, 
                                       f.func_name, 
                                       f.func.func_defaults, 
                                       f.func_closure) 
