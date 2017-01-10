from string import digits, ascii_letters

try:
    import maya.cmds as cmds
except ImportError:
    print 'WARNING (%s): failed to load maya.cmds module.' % __file__

from .pure import cmap, grep


# PURE

validNameChars = digits + ascii_letters
toValidMayaName = lambda name: ''.join(cmap(lambda x: x if x in validNameChars else '_')(name))

withNS = lambda ns: lambda x: ns + ":" + x


# IMPURE

scenePath = lambda: cmds.file(query=True, sceneName=True)
sceneName = lambda: scenePath().split('/')[-1]

grepScene = lambda pat: grep(pat)(cmds.ls(allPaths=True))

obExists = lambda x: cmds.objExists(x)

