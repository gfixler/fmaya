from itertools import count

cmap = lambda f: lambda xs: (f(x) for x in xs)

lazy = lambda xs: (x for x in xs)
strict = list

grid2D = lambda w: ((x, y) for y in count(0) for x in xrange(w))

ab2abx = lambda x: lambda (a, b): (a, b, x)

czip = lambda xs: lambda ys: (x for x in zip(xs, ys))
zipWith = lambda f: lambda xs: lambda ys: (f(x)(y) for (x, y) in czip(xs)(ys))

loc = lambda: cmds.spaceLocator()[0]
moveTo = lambda xyz: lambda tf: cmds.xform(tf, worldSpace=True, translation=xyz)
spawnAt = lambda xyz: lambda f: moveTo(xyz)(f())
locAt = flip(spawnAt)(loc)

flip = lambda f: lambda x: lambda y: f(y)(x)


take = lambda n: lambda xs: (xs.next() for i in xrange(n))

gridXY0 = lambda w: cmap(ab2abx(0))(grid2D(w))

gridXY0_ = lambda x: lambda y: take(x * y)(gridXY0(x))

strict(cmap(locAt)(gridXY0_(10)(15)))

g = grid2D(5)
ab2abx(0)(g.next())


