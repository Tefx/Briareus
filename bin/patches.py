import types

def map(f, l):
	if isinstance(f, types.BuiltinFunctionType):
		return [f(x) for x in l]
