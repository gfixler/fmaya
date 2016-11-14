try:
    import maya.cmds as cmds
except ImportError:
    print 'WARNING (%s): failed to load maya.cmds module.' % __file__

from .pure import comp, cmap, uncurry, snd, mid, preadd, noneToEmpty


# PURE

nodeFromChannel = lambda channel: channel.split('.')[0]
attrFromChannel = lambda channel: channel.split('.')[-1]
chanFromChannel = lambda channel: (nodeFromChannel(channel), attrFromChannel(channel))
attrToChannel = lambda node: preadd(node + ".")

minAndMax = lambda xs: (min(xs), max(xs)) # non-total: fails on empty list
keysValueRange = lambda keys: minAndMax(cmap(snd)(keys)) # non-total: fails on empty keys list
keysMedianValue = comp(uncurry(mid), keysValueRange) # non-total: fails on empty keys list


# IMPURE

curTime = lambda: cmds.currentTime(query=True)

attrType = lambda channel: cmds.getAttr(channel, type=True)

getChannelAtTime = lambda time: lambda channel: cmds.getAttr(channel, time=time)
getChannel = getChannelAtTime(cmds.currentTime(query=True))

getKeyTimes = lambda channel: noneToEmpty(cmds.keyframe(channel, query=True, timeChange=True))
getKeyValues = lambda channel: noneToEmpty(cmds.keyframe(channel, query=True, valueChange=True))
getKeys = lambda channel: zip(getKeyTimes(channel), getKeyValues(channel))

artistChannels = lambda node: cmap(attrToChannel(node))(cmds.listAttr(node, keyable=True, visible=True, unlocked=True))

numericChannelTypes = ['doubleLinear','doubleAngle','double']
isNumericChannel = lambda channel: attrType(channel) in numericChannelTypes
numericArtistChannels = lambda node: filter(isNumericChannel, artistChannels(node)) # non-total: fails on empty list

