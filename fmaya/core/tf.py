try:
    import maya.cmds as cmds
except ImportError:
    print 'WARNING (%s): failed to load maya.cmds module.' % __file__


# PURE

xyzAdd = lambda (x,y,z): lambda (u,v,w): (x+u, y+v, z+w)
xyzSub = lambda (x,y,z): lambda (u,v,w): (x-u, y-v, z-w)
xyzMul = lambda (x,y,z): lambda (u,v,w): (x*u, y*v, z*w)

