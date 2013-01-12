import ast
import unparse


class NamesMapper(ast.NodeTransformer):
    def __init__(self, maps):
        super(NamesMapper, self).__init__()
        self.maps = maps

    def visit_Name(self, node):
        if node.id in self.maps:
            return self.maps[node.id]
        else:
            return node

class ASTModifier(ast.NodeTransformer):
    def __init__(self, tokens):
        super(ASTModifier, self).__init__()
        self.var_count = 0
        self.tokens = tokens

    def make_name(self, prefix):
        name = "%s%d" % (prefix, self.var_count)
        self.var_count += 1
        return name

    def map_args(self, arg_items, body):
        if len(arg_items) == 1:
            arg = ast.arguments(args=[arg_items[0]], vararg=None, kwarg=None, defaults=[])
            return arg, body
        arg = ast.Name(id=self.make_name("_a"), ctx=ast.Load())
        maps = self.get_slice(arg, arg_items)
        if isinstance(body, list):
            body = [NamesMapper(maps).visit(i) for i in body]
        else:
            body = NamesMapper(maps).visit(body)
        arg = ast.arguments(args=[arg], vararg=None, kwarg=None, defaults=[])
        return arg, body

    def func_var_names(self, ast_node):
        node = ast.fix_missing_locations(ast_node)
        funcion_name = ast_node.name
        module = ast.Module(body=[ast_node])
        ctx = {}
        code = compile(module, '<string>', 'exec')
        eval(code, {}, ctx)
        function = ctx[funcion_name]
        return function.func_code.co_varnames
        

    def func_def(self, arg_items, body):
        args, body = self.map_args(arg_items, body)
        # body.append(ast.Return(value=ast.Call(func=ast.Name(id='locals', ctx=ast.Load()), args=[], keywords=[], starargs=None, kwargs=None)))
        name = self.make_name("_f")
        func = ast.FunctionDef(name=name, args=args, body=body, decorator_list=[])
        var_names = self.func_var_names(func)
        args_names = [arg.id for arg in args.args]
        global_names = [x for x in var_names if x not in args_names]
        if global_names:
            body = [ast.Global(names=global_names)] + body
        func = ast.FunctionDef(name=name, args=args, body=body, decorator_list=[])
        return name, func

    def map_func(self, func, iterable):
        return ast.Call(func=ast.Name(id='_pmap', ctx=ast.Load()), args=[func]+iterable, keywords=[], starargs=None, kwargs=None)

    def map_and_export(self, func, iterable):
        map_call = self.map_func(func, iterable)
        return ast.Call(func=ast.Name(id='_export', ctx=ast.Load()), args=[map_call], keywords=[], starargs=None, kwargs=None)

    def find_For_deepth(self, for_tree):
        yield for_tree.target, for_tree.iter
        if len(for_tree.body) == 1 and isinstance(for_tree.body[0], ast.For):
            for x in self.find_For_deepth(for_tree.body[0]):
                yield x
        else:
            yield for_tree.body

    def visit_For(self, for_tree):
        if for_tree.lineno not in self.tokens:
            return for_tree
        for node in ast.walk(for_tree):
            if isinstance(node, ast.Yield) or isinstance(node, ast.Return):
                return for_tree
        iters = [x for x in self.find_For_deepth(for_tree)]
        body = iters[-1]
        iters = iters[:-1]
        iterable = [self.product_func([x[1] for x in iters])]
        f_name, f_tree = self.func_def([x[0] for x in iters], body)
        func = ast.Name(id=f_name, ctx=ast.Load())
        map_tree = ast.Expr(value=self.map_func(func, iterable))
        return f_tree, map_tree

    def get_slice(self, src, args):
        maps = {}
        for i in xrange(len(args)):
            if isinstance(args[i], ast.Tuple):
                src_1 = ast.Subscript(value=src, slice=ast.Index(value=ast.Num(n=i)), ctx=ast.Load())
                maps.update(self.get_slice(src_1, args[i].elts))
            elif isinstance(args[i], ast.Name):
                maps[args[i].id] = ast.Subscript(value=src, slice=ast.Index(value=ast.Num(n=i)), ctx=ast.Load())
        return maps

    def visit_ListComp(self, node):
        if node.lineno not in self.tokens:
            return node
        arg_items = [x.target for x in node.generators]
        args, node = self.map_args(arg_items, node)
        iters = [x.iter for x in node.generators]
        filters = []
        for item in node.generators:
            if item.ifs:
                filters.append(ast.Lambda(args=args, body=item.ifs))
            else:
                filters.append(ast.Name(id='None', ctx=ast.Load()))
        if len(iters) == 1:
            if getattr(filters[0], "id", None) == "None":
                iterable = iters[0]
            else:
                iterable = ast.Call(func=ast.Name(id='filter', ctx=ast.Load()), args=[filters[0], iters[0]], keywords=[], starargs=None, kwargs=None)
        else:
            iterable = self.listcomp_func(iters, filters)
        return self.map_func(ast.Lambda(args=args, body=node.elt), [iterable])


    def product2_func(self, iters, filters):
        iters = ast.List(elts=iters, ctx=ast.Load())
        filters = ast.List(elts=filters, ctx=ast.Load())
        return ast.Call(func=ast.Name(id='_product2', ctx=ast.Load()), args=[iters, filters], keywords=[], starargs=None, kwargs=None)

    def product_func(self, iters):
        return ast.Call(func=ast.Name(id='_product', ctx=ast.Load()), args=iters, keywords=[], starargs=None, kwargs=None)
