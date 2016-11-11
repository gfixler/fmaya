import maya.cmds as cmds
import maya.mel as mel


selection = lambda: (lambda xs: xs if xs else [])(cmds.ls(selection=True, flatten=True))
selection1 = lambda: sel()[0] # non-total; errors on empty selection

channelBoxSelection = lambda: mel.eval("channelBox -query -selectedMainAttributes $gChannelBoxName;")

