from gevent import monkey; monkey.patch_all()
import gevent
import inspect
from ..config import config


def import_globals():
    frame, outerframe = [x[0] for x in inspect.getouterframes(inspect.currentframe())[1:3]]
    frame.f_globals.update(outerframe.f_globals)

def pmap(f, l):
    lets = []
    for i in l:
        lets.append(gevent.spawn(f, i))
    gevent.joinall(lets)
    return [i.value for i in lets]

def export(ls):
    frame = inspect.getouterframes(inspect.currentframe())[1][0]
    for item in ls:
        frame.f_globals.update(item)

def product(*args):
    if len(args) == 1:
        return args[0]
    result = [[]]
    for arg in args:
        result = [x+[y] for x in result for y in arg]
    return result

def product2(iters, filters):
    result = [[]]
    for item, f in zip(iters, filters):
        if f:
            result = [x+[y] for x in result for y in item if f(x+[y])]
        else:
            result = [x+[y] for x in result for y in item]
    return result


if __name__ == '__main__':
    print product(range(10))



