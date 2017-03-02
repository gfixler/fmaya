from math import sqrt

const = lambda x: lambda _: x

uncurry2 = lambda f: lambda x, y: f(x)(y)

getPos = lambda tf: tuple(cmds.xform(tf, query=True, translation=True))
setPos = lambda tf: lambda xyz: cmds.xform(tf, translation=xyz)

getRot = lambda tf: tuple(cmds.xform(tf, query=True, rotation=True))
setRot = lambda tf: lambda xyz: cmds.xform(tf, rotation=xyz)

getWSPos = lambda tf: tuple(cmds.xform(tf, query=True, worldSpace=True, translation=True))
setWSPos = lambda tf: lambda xyz: cmds.xform(tf, worldSpace=True, translation=xyz)

getWSRot = lambda tf: tuple(cmds.xform(tf, query=True, worldSpace=True, rotation=True))
setWSRot = lambda tf: lambda xyz: cmds.xform(tf, worldSpace=True, rotation=xyz)

xyzAdd = lambda (x, y, z): lambda (u, v, w): (x + u, y + v, z + w)
xyzSub = lambda (x, y, z): lambda (u, v, w): (x - u, y - v, z - w)
xyzMul = lambda (x, y, z): lambda (u, v, w): (x * u, y * v, z * w)
xyzDiv = lambda (x, y, z): lambda (u, v, w): (x / u, y / v, z / w)
xyzScale = lambda s: xyzMul((s,s,s))
xyzAvg = lambda xs: xyzScale(1.0/len(xs))(reduce(uncurry2(xyzSub), xs, (0, 0, 0)))
xyzDist = lambda (x, y, z): lambda (u, v, w): sqrt((x+u)*(x+u)+(y+v)*(y+v)+(z+w)*(z+w))
xyzHypot = xyzDist((0, 0, 0))
xyzUnit = lambda (x, y, z): (lambda d: (x/d, y/d, z/d))(xyzHypot(xyz))


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
        smlf.xyz = (lambda (x,y,z): (x,y,value))(self.xyz)

    def __repr__ (self):
        return ("V3 " + str(self.xyz))

    def __neg__ (self):
        return V3(xyzMul(self.xyz)((-1,-1,-1)))

    def __add__ (self, other):
        if type(other) == int or type(other) == float:
            return V3(xyzAdd(self.xyz)((other,other,other)))
        else:
            return V3(xyzAdd(self.xyz)(other.xyz))

    def __radd__ (self, other):
        return self.__add__(other)

    def __sub__ (self, other):
        if type(other) == int or type(other) == float:
            return V3(xyzSub(self.xyz)((other,other,other)))
        else:
            return V3(xyzSub(self.xyz)(other.xyz))

    def __rsub__ (self, other):
        return self.__sub__(other)

    def __mul__ (self, other):
        if type(other) == int or type(other) == float:
            return V3(xyzMul(self.xyz)((other,other,other)))
        else:
            return V3(xyzMul(self.xyz)(other.xyz))

    def __rmul__ (self, other):
        return self.__mul__(other)

    def __div__ (self, other):
        if type(other) == int or type(other) == float:
            return V3(xyzDiv(self.xyz)((other,other,other)))
        else:
            return V3(xyzDiv(self.xyz)(other.xyz))

    def __rdiv__ (self, other):
        return self.__div__(other)

    def mag (self):
        return xyzHypot(self.xyz)

    def unit (self):
        return self / self.mag()


v3T = lambda tf: V3(getWSPos(tf))
v3R = lambda tf: V3(getWSRot(tf))

