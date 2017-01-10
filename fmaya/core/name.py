# PURE

withNS = lambda ns: lambda x: ns + ":" + x
stripNS = lambda x: x.split(":")[-1]

