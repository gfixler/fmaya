try:
    import maya.cmds as cmds
except ImportError:
    print 'WARNING (%s): failed to load maya.cmds module.' % __file__

from .pure import _not, comp, cmap, isEmpty, uncurryPair, snd, mid, preadd, emptyNone
from .scene import getTime


# PURE

nodeFromChannel = lambda channel: channel.split('.')[0]
attrFromChannel = lambda channel: channel.split('.')[-1]
chanFromChannel = lambda channel: (nodeFromChannel(channel), attrFromChannel(channel))
attrToChannel = lambda node: preadd(node + ".")

minAndMax = lambda xs: (min(xs), max(xs)) # non-total: fails on empty list
keysValueRange = lambda keys: minAndMax(cmap(snd)(keys)) # non-total: fails on empty keys list
keysValueCenter = comp(uncurryPair(mid), keysValueRange) # non-total: fails on empty keys list


# IMPURE

getAttrType = lambda channel: cmds.getAttr(channel, type=True)

getChannelAtTime = lambda time: lambda channel: cmds.getAttr(channel, time=time)
getChannel = comp(getChannelAtTime, getTime)

setChannel = lambda c: lambda (t, v): cmds.setKeyframe(c, time=t, value=v)

getKeyTimes = lambda channel: emptyNone(cmds.keyframe(channel, query=True, timeChange=True))
getKeyValues = lambda channel: emptyNone(cmds.keyframe(channel, query=True, valueChange=True))
getKeys = lambda channel: zip(getKeyTimes(channel), getKeyValues(channel))

hasKeys = comp(_not, isEmpty, getKeyTimes)

artistAttrs = lambda node: cmds.listAttr(node, keyable=True, visible=True, unlocked=True) or []
artistChannels = lambda node: cmap(attrToChannel(node))(artistAttrs(node))

numericChannelTypes = ['doubleLinear','doubleAngle','double']
isNumericChannel = lambda channel: getAttrType(channel) in numericChannelTypes
numericArtistChannels = lambda node: filter(isNumericChannel, artistChannels(node))

