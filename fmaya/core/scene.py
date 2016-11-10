from string import digits, ascii_letters

validNameChars = digits + ascii_letters
toValidMayaName = lambda name: ''.join(cmap(lambda x: x if x in validNameChars else '_')(name))

