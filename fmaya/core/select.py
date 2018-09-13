try:
    import maya.cmds as cmds
except ImportError:
    print 'WARNING (%s): failed to load maya.cmds module.' % __file__

try:
    import maya.mel as mel
except ImportError:
    print 'WARNING (%s): failed to load maya.mel module.' % __file__


# IMPURE

grab = lambda *args, **kwargs: cmds.select(*args, **kwargs)

sel = lambda: cmds.ls(selection=True, flatten=True) or []
sel1 = lambda: sel()[0] # non-total; errors on empty selection

channelBoxSelection = lambda: mel.eval("channelBox -query -selectedMainAttributes $gChannelBoxName;")

