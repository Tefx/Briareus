from gevent import monkey; monkey.patch_all()
from Lazy import LazyDict, AsyncCallable
from Cloud import utils as CloudUtils
from Parallel import utils as ParaUtils
from Face import modify
import inspect


def setup(only_gen_source=False):
    frame, path, line = inspect.getouterframes(inspect.currentframe())[1][:3]
    tree = modify(path, line, only_gen_source)
    if only_gen_source:
        print tree
        exit(0)
    new_gloabls = LazyDict(frame.f_globals)
    new_gloabls.update({"_product" : ParaUtils.product,
                        "_product2" : ParaUtils.product2,
                        "_pmap" : ParaUtils.pmap,
                        "_export": ParaUtils.export,
                        "_cloud": CloudUtils.Cloud,
                        "_cached": CloudUtils.CachedData,
                        "_async": AsyncCallable})
    code = compile(tree, 'path', 'exec')
    exec code in new_gloabls
    exit(0)