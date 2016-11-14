try:
    import maya.cmds as cmds
except ImportError:
    print 'WARNING (%s): failed to load maya.cmds module.' % __file__

try:
    import maya.mel as mel
except ImportError:
    print 'WARNING (%s): failed to load maya.mel module.' % __file__


selection = lambda: (lambda xs: xs if xs else [])(cmds.ls(selection=True, flatten=True))
selection1 = lambda: selection()[0] # non-total; errors on empty selection

channelBoxSelection = lambda: mel.eval("channelBox -query -selectedMainAttributes $gChannelBoxName;")

