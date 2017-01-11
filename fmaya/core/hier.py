try:
    import maya.cmds as cmds
except ImportError:
    print 'WARNING (%s): failed to load maya.cmds module.' % __file__


getParent = lambda x: (lambda y: y[0] if y else None)(cmds.listRelatives(x, parent=True))
parentPred = lambda p: lambda x: (lambda y: p(y) if y else False)(getParent(x))

