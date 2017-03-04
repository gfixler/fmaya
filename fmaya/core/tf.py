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
xyzHypot = xyzDist((0,0,0))
xyzUnit = lambda xyz: xyzScale(1.0/xyzHypot(xyz))(xyz)


class V3 (object):

    def __init__ (self, xyz=(0,0,0)):
        self.xyz = tuple(xyz)

    @property
    def x (self):
        return (lambda (x,y,z): x)(self.xyz)

    @x.setter
    def x (self, value):
        self.xyz = (lambda (x,y,z): (value,y,z))(self.xyz)

    @property
    def y (self):
        return (lambda (x,y,z): y)(self.xyz)

    @y.setter
    def y (self, value):
        self.xyz = (lambda (x,y,z): (x,value,z))(self.xyz)

    @property
    def z (self):
        return (lambda (x,y,z): z)(self.xyz)

    @z.setter
    def z (self, value):
        self.xyz = (lambda (x,y,z): (x,y,value))(self.xyz)

    def __repr__ (self):
        return ("V3 " + str(self.xyz))

    def __eq__ (self, other):
        return self.xyz == other.xyz

    def __ne__ (self, other):
        return (self.xyz != other.xyz)

    def __add__ (self, other):
        return V3(xyzAdd(self.xyz)(other.xyz))

    def __sub__ (self, other):
        return V3(xyzSub(self.xyz)(other.xyz))

    def __mul__ (self, other):
        return V3(xyzMul(self.xyz)(other.xyz))


# IMPURE

getPos = lambda tf: tuple(cmds.xform(tf, query=True, translation=True))
setPos = lambda tf: lambda xyz: cmds.xform(tf, translation=xyz)

getWSPos = lambda tf: tuple(cmds.xform(tf, query=True, worldSpace=True, translation=True))
setWSPos = lambda tf: lambda xyz: cmds.xform(tf, worldSpace=True, translation=xyz)

getRot = lambda tf: tuple(cmds.xform(tf, query=True, rotation=True))
setRot = lambda tf: lambda xyz: cmds.xform(tf, rotation=xyz)

getWSRot = lambda tf: tuple(cmds.xform(tf, query=True, worldSpace=True, rotation=True))
setWSRot = lambda tf: lambda xyz: cmds.xform(tf, worldSpace=True, rotation=xyz)

