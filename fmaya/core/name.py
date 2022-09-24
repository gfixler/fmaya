try:
    import maya.cmds as cmds
except ImportError:
    print 'WARNING (%s): failed to load maya.cmds module.' % __file__

from pure import const, cmap

from string import digits, ascii_letters


# PURE

validNameChars = digits + ascii_letters
toValidMayaName = lambda name: ''.join(cmap(lambda x: x if x in validNameChars else '_')(name))

withNS = lambda ns: lambda x: ns + ":" + x
stripNS = lambda x: x.split(":")[-1]


# IMPURE

renameBy = lambda f: lambda n: cmds.rename(n, f(n))
renameTo = lambda n: renameBy(const(n))

