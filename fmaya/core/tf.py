from math import sqrt

try:
    import maya.cmds as cmds
except ImportError:
    print 'WARNING (%s): failed to load maya.cmds module.' % __file__

from .pure import uncurry


# PURE

xyzAdd = lambda (x,y,z): lambda (u,v,w): (x+u, y+v, z+w)
xyzSub = lambda (x,y,z): lambda (u,v,w): (x-u, y-v, z-w)
xyzMul = lambda (x,y,z): lambda (u,v,w): (x*u, y*v, z*w)
xyzDiv = lambda (x,y,z): lambda (u,v,w): (float(x)/float(u), float(y)/float(v), (z)/float(w))
xyzScale = lambda s: lambda (x,y,z): (s*x, s*y, s*z)
xyzSum = lambda xs: (0,0,0) if len(xs) == 0 else reduce(uncurry(xyzAdd), xs, (0,0,0))
xyzAvg = lambda xs: (0,0,0) if len(xs) == 0 else xyzSum(map(xyzScale(1.0/len(xs)), xs))
xyzDist = lambda (x,y,z): lambda (u,v,w): sqrt((x-u) * (x-u) + (y-v) * (y-v) + (z-w) * (z-w))

