flip = lambda f: lambda x: lambda y: f(y)(x)
cmap = lambda f: lambda xs: map(f, xs)
uncurryPair = lambda f: lambda (x, y): f(x)(y)
dot = lambda a: lambda b: a + "." + b

def say (msg):
    print msg

retnone = lambda f: lambda x: [None, f(x)][0]
preach = cmap(say)
preach_ = retnone(preach)

"""
map(flip(dot)("tx"), ["persp", "top", "front", "side"])
"""

ball = lambda r: lambda p: lambda n: "Made a ball named '" + n + "' of radius " + str(r) + " at position " + str(p) + "."

ball(0.3)((1,2,3))("Larry")

"""
doBalls = cmap(uncurryPair(ball(0.3)))
preach_(doBalls([((1,2,3),"Larry"), ((3,3,2), "Janice"), ((0,0,1), "Karen")]))
"""

