# PURE

nodeFromChannel = lambda channel: channel.split('.')[0]
attrFromChannel = lambda channel: channel.split('.')[-1]
chanFromChannel = lambda channel: (nodeFromChannel(channel), attrFromChannel(channel))
attrToChannel = lambda node: preadd(node + ".")


# IMPURE

getChannelAtTime = lambda time: lambda channel: cmds.getAttr(channel, time=time)
getChannel = getChannelAtTime(cmds.currentTime(query=True))

