nodeFromChannel = lambda channel: channel.split('.')[0]
attrFromChannel = lambda channel: channel.split('.')[-1]
chanFromChannel = lambda channel: (nodeFromChannel(channel), attrFromChannel(channel))
attrToChannel = lambda node: preadd(node + ".")

