from itertools import count

lazy = lambda xs: (x for x in xs)
strict = list

czip = lambda xs: lambda ys: zip(xs, ys)
zzip = lambda xs: lambda ys: ((x, y) for (x, y) in zip(xs, ys))

zipWith = lambda f: lambda xs: lambda ys: cmap(uncurryPair(f))(czip(xs)(ys))

loc = lambda: cmds.spaceLocator()[0]

moveTo = lambda xyz: lambda tf: cmds.xform(tf, worldSpace=True, translation=xyz)
spawnAt = lambda xyz: lambda f: moveTo(xyz)(f())

doTimes = lambda n: lambda f: (f() for _ in xrange(n))

xyz2xzy = lambda (x, y, z): (x, z, y)
xyz2yxz = lambda (x, y, z): (y, x, z)
xyz2yzx = lambda (x, y, z): (y, z, x)
xyz2zxy = lambda (x, y, z): (z, x, y)
xyz2zyx = lambda (x, y, z): (z, y, x)

grid2D = lambda w: ((x, y) for y in count() for x in xrange(w))

take = lambda n: lambda xs: (xs.next() for _ in xrange(n))
drop = lambda n: lambda xs: [take(n)(xs), xs][-1]

"""
take(5)(grid2D(5))
take(5)(drop(2)(grid2D(5)))

take(5)(lazy("this is a test"))
strict(doTimes(5)(loc))
""

