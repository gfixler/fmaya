import maya.cmds as cmds

from .pure import preadd, noneToEmpty

# PURE

nodeFromChannel = lambda channel: channel.split('.')[0]
attrFromChannel = lambda channel: channel.split('.')[-1]
chanFromChannel = lambda channel: (nodeFromChannel(channel), attrFromChannel(channel))
attrToChannel = lambda node: preadd(node + ".")


# IMPURE

getChannelAtTime = lambda time: lambda channel: cmds.getAttr(channel, time=time)
getChannel = getChannelAtTime(cmds.currentTime(query=True))

getKeyTimes = lambda channel: noneToEmpty(cmds.keyframe(channel, query=True, timeChange=True))
getKeyValues = lambda channel: noneToEmpty(cmds.keyframe(channel, query=True, valueChange=True))
getKeys = lambda channel: zip(getKeyTimes(channel), getKeyValues(channel))

