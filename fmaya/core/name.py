try:
    import maya.cmds as cmds
except ImportError:
    print 'WARNING (%s): failed to load maya.cmds module.' % __file__


# PURE

stripNS = lambda x: x.split(":")[-1]

