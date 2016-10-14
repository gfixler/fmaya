ident = lambda x: x
const = lambda x: lambda _: x

curry = lambda f: lambda x: lambda y: f(x, y)
uncurry = lambda f: lambda x, y: f(x)(y)

