from math import sqrt

try:
    import maya.cmds as cmds
except ImportError:
    print 'WARNING (%s): failed to load maya.cmds module.' % __file__

from pure import both, uncurry2


# PURE

xyzAdd = lambda (x,y,z): lambda (u,v,w): (x+u, y+v, z+w)
xyzSub = lambda (x,y,z): lambda (u,v,w): (x-u, y-v, z-w)
xyzMul = lambda (x,y,z): lambda (u,v,w): (x*u, y*v, z*w)
xyzDiv = lambda (x,y,z): lambda (u,v,w): (float(x)/float(u), float(y)/float(v), (z)/float(w))
xyzScale = lambda s: lambda (x,y,z): (s*x, s*y, s*z)
xyzSum = lambda xs: (0,0,0) if len(xs) == 0 else reduce(uncurry2(xyzAdd), xs, (0,0,0))
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

