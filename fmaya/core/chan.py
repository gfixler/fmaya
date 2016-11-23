try:
    import maya.cmds as cmds
except ImportError:
    print 'WARNING (%s): failed to load maya.cmds module.' % __file__

from .pure import comp, cmap, uncurry, snd, mid, preadd, emptyNone


# PURE

nodeFromChannel = lambda channel: channel.split('.')[0]
attrFromChannel = lambda channel: channel.split('.')[-1]
chanFromChannel = lambda channel: (nodeFromChannel(channel), attrFromChannel(channel))
attrToChannel = lambda node: preadd(node + ".")

minAndMax = lambda xs: (min(xs), max(xs)) # non-total: fails on empty list
keysValueRange = lambda keys: minAndMax(cmap(snd)(keys)) # non-total: fails on empty keys list
keysValueCenter = comp(uncurry(mid), keysValueRange) # non-total: fails on empty keys list


# IMPURE

getTime = lambda: cmds.currentTime(query=True)

getAttrType = lambda channel: cmds.getAttr(channel, type=True)

getChannelAtTime = lambda time: lambda channel: cmds.getAttr(channel, time=time)
getChannel = comp(getChannelAtTime, getTime)

getKeyTimes = lambda channel: emptyNone(cmds.keyframe(channel, query=True, timeChange=True))
getKeyValues = lambda channel: emptyNone(cmds.keyframe(channel, query=True, valueChange=True))
getKeys = lambda channel: zip(getKeyTimes(channel), getKeyValues(channel))

artistChannels = lambda node: cmap(attrToChannel(node))(cmds.listAttr(node, keyable=True, visible=True, unlocked=True))

numericChannelTypes = ['doubleLinear','doubleAngle','double']
isNumericChannel = lambda channel: getAttrType(channel) in numericChannelTypes
numericArtistChannels = lambda node: filter(isNumericChannel, artistChannels(node)) # non-total: fails on empty list

