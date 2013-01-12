import cStringIO as StringIO
from token_mod import TokenModifier
from ast_mod import ASTModifier
import ast

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
        unparse.Unparser(tree, string)
        return string.getvalue()
    else:
        return tree