ident = lambda x: x
const = lambda x: lambda _: x
comp = lambda *fs: reduce(lambda f, g: lambda x: f(g(x)), fs, ident)
cmap = lambda f: lambda xs: map(f, xs)

curry = lambda f: lambda x: lambda y: f(x, y)
uncurry = lambda f: lambda (x, y): f(x)(y)

fst = lambda (x, _): x
snd = lambda (_, y): y

concat = lambda xss: [x for xs in xss for x in xs]
noneToEmpty = lambda xs: xs or []
isEmpty = lambda xs: xs == []

bnot = lambda b: not b
eq = lambda a: lambda b: a == b
neq = lambda a: comp(bnot, eq(a))

preadd = lambda p: lambda s: p + s
postadd = lambda p: lambda s: s + p

mid = lambda a: lambda b: (a + b) / 2

filt = lambda f: lambda xs: filter(f, xs)

