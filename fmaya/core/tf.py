from math import sqrt

try:
    import maya.cmds as cmds
except ImportError:
    print 'WARNING (%s): failed to load maya.cmds module.' % __file__

from pure import both, uncurry2


# PURE

xyzAdd = lambda a: lambda b: (a[0]+b[0], a[1]+b[1], a[2]+b[2])
xyzSub = lambda a: lambda b: (a[0]-b[0], a[1]-b[1], a[2]-b[2])
xyzMul = lambda a: lambda b: (a[0]*b[0], a[1]*b[1], a[2]*b[2])
xyzDiv = lambda a: lambda b: (float(a[0])/float(b[0]), float(a[1])/float(b[1]), (a[2])/float(b[2]))
xyzScale = lambda s: lambda p: (s*p[0], s*p[1], s*p[2])
xyzSum = lambda xs: (0,0,0) if len(xs) == 0 else reduce(uncurry2(xyzAdd), xs, (0,0,0))
xyzAvg = lambda xs: (0,0,0) if len(xs) == 0 else xyzSum(map(xyzScale(1.0/len(xs)), xs))
xyzDist = lambda a: lambda b: sqrt((a[0]-b[0]) * (a[0]-b[0]) + (a[1]-b[1]) * (a[1]-b[1]) + (a[2]-b[2]) * (a[2]-b[2]))
xyzHypot = xyzDist((0,0,0))
xyzUnit = lambda xyz: xyzScale(1.0/xyzHypot(xyz))(xyz)


class V3 (object):

    def __init__ (self, xyz=(0,0,0)):
        self.xyz = tuple(xyz)

    @property
    def x (self):
        return (lambda v: v[0])(self.xyz)

    @x.setter
    def x (self, value):
        self.xyz = (lambda v: (value,v[1],v[2]))(self.xyz)

    @property
    def y (self):
        return (lambda v: v[1])(self.xyz)

    @y.setter
    def y (self, value):
        self.xyz = (lambda v: (v[0],value,v[2]))(self.xyz)

    @property
    def z (self):
        return (lambda v: v[2])(self.xyz)

    @z.setter
    def z (self, value):
        self.xyz = (lambda v: (v[0],v[1],value))(self.xyz)

    def __repr__ (self):
        return ("V3 " + str(self.xyz))

    def __eq__ (self, other):
        return self.xyz == other.xyz

    def __ne__ (self, other):
        return (self.xyz != other.xyz)

    def __add__ (self, other):
        if type(other) == int or type(other) == float:
            return V3(xyzAdd(self.xyz)((other,other,other)))
        else:
            return V3(xyzAdd(self.xyz)(other.xyz))

    def __radd__ (self, other):
        return self.__add__(other)

    def __sub__ (self, other):
        return V3(xyzSub(self.xyz)(other.xyz))

    def __mul__ (self, other):
        if type(other) == int or type(other) == float:
            return V3(xyzMul(self.xyz)((other,other,other)))
        else:
            return V3(xyzMul(self.xyz)(other.xyz))

    def __rmul__ (self, other):
        return self.__mul__(other)

    def __div__ (self, other):
        if type(other) == int or type(other) == float:
            return V3(xyzMul(self.xyz)((1.0/other,1.0/other,1.0/other)))
        else:
            return V3(xyzDiv(self.xyz)(other.xyz))

    def mag (self):
        return xyzHypot(self.xyz)

    def unit (self):
        return self * (1 / self.mag())


v3Avg = lambda vs: V3([]) if len(vs) == 0 else sum(vs) / len(vs)
v3Mid = lambda a: lambda b: v3Avg([a,b])


# IMPURE

pos = lambda tf: tuple(cmds.xform(tf, query=True, translation=True))
rot = lambda tf: tuple(cmds.xform(tf, query=True, rotation=True))
posrot = both(pos)(rot)

wpos = lambda tf: tuple(cmds.xform(tf, query=True, worldSpace=True, translation=True))
wrot = lambda tf: tuple(cmds.xform(tf, query=True, worldSpace=True, rotation=True))
wposrot = both(wpos)(wrot)

setpos = lambda tf: lambda xyz: cmds.xform(tf, translation=xyz)
setrot = lambda tf: lambda xyz: cmds.xform(tf, rotation=xyz)

setwpos = lambda tf: lambda xyz: cmds.xform(tf, worldSpace=True, translation=xyz)
setwrot = lambda tf: lambda xyz: cmds.xform(tf, worldSpace=True, rotation=xyz)

