const = lambda x: lambda _: x

uncurry2 = lambda f: lambda x, y: f(x)(y)

getPos = lambda tf: cmds.xform(tf, query=True, translation=True)
setPos = lambda tf: lambda xyz: cmds.xform(tf, translation=xyz)

getRot = lambda tf: cmds.xform(tf, query=True, rotation=True)
setRot = lambda tf: lambda xyz: cmds.xform(tf, rotation=xyz)

getWSPos = lambda tf: cmds.xform(tf, query=True, worldSpace=True, translation=True)
setWSPos = lambda tf: lambda xyz: cmds.xform(tf, worldSpace=True, translation=xyz)

getWSRot = lambda tf: cmds.xform(tf, query=True, worldSpace=True, rotation=True)
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


class TForm (object):

    def __init__ (self, locT=(0,0,0), worldT=(0,0,0), locR=(0,0,0), worldR=(0,0,0)):
        self.locT = locT
        self.worldT = worldT
        self.locR = locR
        self.worldR = worldR

    def getLocal (self, tf):
        self.locT = getPos(tf)
        self.locR = getRot(tf)

    def getWorld (self, tf):
        self.worldT = getWSPos(tf)
        self.worldR = getWSRot(tf)

    def get (self, tf):
        self.getLocal(tf)
        self.getWorld(tf)

    def setLocalT (self, tf):
        setPos(tf)(self.locT)

    def setWorldT (self, tf):
        setWSPos(tf)(self.worldT)

    def setT (self, tf):
        self.setLocalT(tf)
        self.setWorldT(tf)

    def setLocalR (self, tf):
        setRot(tf)(self.locR)

    def setWorldR (self, tf):
        setWSRot(tf)(self.worldR)

    def setR (self, tf):
        self.setLocalR(tf)
        self.setWorldR(tf)

    def set (self, tf):
        self.setT(tf)
        self.setR(tf)

    def __neg__ (self):
        return TForm ( xyzMul(self.locT)((-1, -1, -1))
                     , xyzMul(self.worldT)((-1, -1, -1))
                     , xyzMul(self.locR)((-1, -1, -1))
                     , xyzMul(self.worldR)((-1, -1, -1))
                     )

    def __add__ (self, other):
        return TForm ( xyzAdd(self.locT)(other.locT)
                     , xyzAdd(self.worldT)(other.worldT)
                     , xyzAdd(self.locR)(other.locR)
                     , xyzAdd(self.worldR)(other.worldR)
                     )

    def __radd__ (self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)

    def __sub__ (self, other):
        return self + -(other)

    def __mul__ (self, other):
        try:
            return TForm ( xyzScale(other)(self.locT)
                         , xyzScale(other)(self.worldT)
                         , xyzScale(other)(self.locR)
                         , xyzScale(other)(self.worldR)
                         )
        except TypeError:
            return TForm ( xyzMul(self.locT)(other.locT)
                         , xyzMul(self.worldT)(other.worldT)
                         , xyzMul(self.locR)(other.locR)
                         , xyzMul(self.worldR)(other.worldR)
                         )

    def __rmul__ (self, other):
        return self.__mul__(other)


fromTF = lambda tf: (lambda inst: const(inst)(inst.get(tf)))(TForm())

