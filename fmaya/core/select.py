import maya.cmds as cmds


selection = lambda: (lambda xs: xs if xs else [])(cmds.ls(selection=True, flatten=True))
selection1 = lambda: sel()[0] # non-total; errors on empty selection

