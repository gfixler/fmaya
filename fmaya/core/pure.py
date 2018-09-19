import re

ident = lambda x: x
const = lambda x: lambda _: x
app = lambda f: lambda x: f(x)
flip = lambda f: lambda x: lambda y: f(y)(x)
juxt = lambda *fs: lambda x: [f(x) for f in fs]
both = lambda f: lambda g: lambda x: (f(x), g(x))
comp = lambda *fs: reduce(lambda f, g: lambda x: f(g(x)), fs, ident)
cmap = lambda f: lambda xs: map(f, xs)
czip = lambda xs: lambda ys: zip(xs, ys)
zipWith = lambda f: lambda xs: lambda ys: [f(x)(y) for (x, y) in zip(xs, ys)]

curry2 = lambda f: lambda x: lambda y: f(x, y)
uncurry2 = lambda f: lambda x, y: f(x)(y)
uncurryPair = lambda f: lambda (x, y): f(x)(y)

fst = lambda (x, _): x
snd = lambda (_, y): y
onFst = lambda f: lambda (x, y): (f(x), y)
onSnd = lambda f: lambda (x, y): (x, f(y))

concat = lambda xss: reduce(lambda x, y: x + y, xss) if xss else []
emptyNone = lambda xs: xs or []
isEmpty = lambda xs: len(xs) == 0

reverse = lambda xs: xs[::-1]

bnot = lambda b: not b
eq = lambda a: lambda b: a == b
neq = lambda a: comp(bnot, eq(a))

begins = lambda b: lambda s: s.startswith(b)
ends = lambda b: lambda s: s.endswith(b)

preadd = lambda p: lambda s: p + s
postadd = lambda p: lambda s: s + p

unprefix = lambda p: lambda s: s[len(p):] if s.startswith(p) else s

mid = lambda a: lambda b: (a + b) / 2.0

filt = lambda f: lambda xs: filter(f, xs)
anyBy = lambda f: lambda xs: any(cmap(f)(xs))

iterateTimes = lambda n: lambda f: lambda x: x if n <= 0 else iterateTimes(n-1)(f)(f(x))

lerp = lambda t: lambda a: lambda b: (b - a) * t + a

grep = lambda pat: lambda xs: [x for x in xs if re.search(pat, x)]

