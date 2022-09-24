from scene import obExists


hasAttr = lambda a: lambda x: obExists(x + "." + a)

