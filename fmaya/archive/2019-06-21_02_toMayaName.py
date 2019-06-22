import string

mayaNameHeadChars = '_' + string.ascii_letters
mayaNameTailChars = mayaHeadChars + string.digits
toMayaNameHead = lambda c: c if c in mayaNameHeadChars else '_'
toMayaNameTail = lambda c: c if c in mayaNameTailChars else '_'
toMayaName = lambda n: ''.join([toMayaNameHead(n[0])] + map(toMayaNameTail, n[1:]))

# toMayaName("My Tool 123!")

