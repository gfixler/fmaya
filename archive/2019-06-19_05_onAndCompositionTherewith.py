comp2 = lambda f: lambda g: lambda x: f(g(x))

on = lambda f: lambda g: lambda x: lambda y: g(f(x))(f(y))

lower = lambda x: x.lower()
upper = lambda x: x.upper()

starts = lambda s: lambda x: x.startswith(s)
ends = lambda e: lambda x: x.endswith(e)
istarts = on(lower)(starts)
iends = on(lower)(ends)

"""
starts("test")("TeStInG")
"""

