from string import digits, ascii_letters

from .pure import cmap


# PURE

validNameChars = digits + ascii_letters
toValidMayaName = lambda name: ''.join(cmap(lambda x: x if x in validNameChars else '_')(name))

withNS = lambda ns: lambda x: ns + ":" + x
stripNS = lambda x: x.split(":")[-1]

