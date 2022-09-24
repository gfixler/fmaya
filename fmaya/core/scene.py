try:
    import maya.cmds as cmds
except ImportError:
    print 'WARNING (%s): failed to load maya.cmds module.' % __file__

from pure import comp, flip, grep, filterBy
from name import withNS


# IMPURE

scenePath = lambda: cmds.file(query=True, sceneName=True)
sceneName = lambda: scenePath().split('/')[-1]

grepScene = lambda pat: grep(pat)(cmds.ls(allPaths=True))

getTime = lambda: cmds.currentTime(query=True)

obExists = lambda x: cmds.objExists(x)

inNS = lambda ns: comp(obExists, withNS(ns))
lsNamespaces = lambda: [":"] + cmds.namespaceInfo(':', listOnlyNamespaces=True, recurse=True)
lsNamespacesContaining = lambda x: filterBy(flip(inNS)(x))(lsNamespaces())


atTime = lambda t: lambda f: lambda x: [cmds.currentTime(t), f(x)][-1]
atTime_ = lambda t: lambda f: [cmds.currentTime(t), f()][-1]

atFrame = lambda t: atTime(round(t))
atFrame_ = lambda t: atTime_(round(t))

inTime = lambda: cmds.playbackOptions(query=True, minTime=True)
outTime = lambda: cmds.playbackOptions(query=True, maxTime=True)

inFrame = lambda: int(round(inTime()))
outFrame = lambda: int(round(outTime()))

allFrames = lambda: xrange(inFrame(), outFrame())

