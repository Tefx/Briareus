import cStringIO as StringIO
from token_mod import TokenModifier
from ast_mod import ASTModifier
import ast


import_str = """
from gevent import monkey; monkey.patch_all()
from Briareus.Parallel.utils import product as _product
from Briareus.Parallel.utils import product2 as _product2
from Briareus.Parallel.utils import pmap as _pmap
from Briareus.Parallel.utils import export as _export
from Briareus.Cloud.utils import Cloud as _cloud
from Briareus.Cloud.utils import CachedData as _cached
from Briareus.Lazy import AsyncCallable as _async
"""


def modify(file_path, pass_lines=0, source=None):
    with open(file_path, "r") as f:
        for x in xrange(pass_lines):
            f.readline()
        tokenMod = TokenModifier(f)
        modified = tokenMod.visit()
        parallel_tokens = getattr(tokenMod, "parallel_token", None)
    tree = ast.parse(modified)
    if parallel_tokens:
        tree = ast.fix_missing_locations(ASTModifier(parallel_tokens).visit(tree))
    if source:
        string = StringIO.StringIO()
        string.write(import_str)
        unparse.Unparser(tree, string)
        return string.getvalue()
    else:
        return tree