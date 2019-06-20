import os

# PURE

ident = lambda x: x
const = lambda x: lambda y: x
comp2 = lambda f: lambda g: lambda x: f(g(x))
juxt = lambda *fs: lambda x: [f(x) for f in fs]
cmap = lambda f: lambda xs: map(f, xs)
inv = lambda f: lambda x: not f(x)

concat = lambda xss: (x for xs in xss for x in xs)

fst = lambda (x, _): x
snd = lambda (_, y): y
onFst = lambda f: lambda (x, y): (f(x), y)
onSnd = lambda f: lambda (x, y): (x, f(y))
fst3 = lambda (x, _, __): x
swap = lambda (x, y): (y, x)

# first = lambda xs: xs[0] # non-total
# last = lambda xs: xs[-1] # non-total

first = lambda d: lambda xs: xs[0] if xs else d
firstBy = lambda f: lambda d: lambda xs: (xs[0] if f(xs[0]) else firstBy(f)(d)(xs[1:])) if xs else d
# first = firstBy(const(True)) # alternative (no default, though)

lt = lambda x: lambda y: y < x
lte = lambda x: lambda y: y <= x
eq = lambda x: lambda y: y == x
gte = lambda x: lambda y: y >= x
gt = lambda x: lambda y: y > x

neq = lambda x: lambda y: y != x

starts = lambda s: lambda x: x.startswith(s)
ends = lambda e: lambda x: x.endswith(e)
contains = lambda c: lambda x: c in x
filt = lambda f: lambda xs: filter(f, xs)

# IMPURE

isType = lambda t: lambda x: cmds.objectType(x) == t

lsMesh = lambda: cmds.ls(type="mesh")
lsJoint = lambda: cmds.ls(type="joint")

lsVert = lambda mesh: cmds.ls(mesh + ".vtx[*]", flatten=True)
lsEdge = lambda mesh: cmds.ls(mesh + ".e[*]", flatten=True)
lsFace = lambda mesh: cmds.ls(mesh + ".f[*]", flatten=True)
lsUV = lambda mesh: cmds.ls(mesh + ".uv[*]", flatten=True)

lsdir = lambda d: os.listdir(d)
jnpath = lambda l: lambda r: os.path.join(l, r)
normpath = lambda path: os.path.normpath(path)
dirwalk = lambda d: os.walk(d)
tree = lambda dir: concat(cmap(comp2(normpath)(jnpath(r)))(fs) for (r, ds, fs) in dirwalk(dir))

open = lambda path: cmds.file(path, open=True, force=True)

