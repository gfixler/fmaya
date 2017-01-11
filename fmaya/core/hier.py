try:
    import maya.cmds as cmds
except ImportError:
    print 'WARNING (%s): failed to load maya.cmds module.' % __file__


getParent = lambda x: (lambda y: y[0] if y else None)(cmds.listRelatives(x, parent=True))
withParent = lambda d: lambda f: lambda x: (lambda y: f(y) if y else d)(getParent(x))
parentPred = withParent(False)

