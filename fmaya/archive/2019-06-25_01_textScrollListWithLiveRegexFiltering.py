import os
import re

comp2 = lambda f: lambda g: lambda x: f(g(x))
cmap = lambda f: lambda xs: map(f, xs)
concat = lambda xss: (x for xs in xss for x in xs)

lsdir = lambda d: os.listdir(d)
jnpath = lambda l: lambda r: os.path.join(l, r)
realpath = lambda path: os.path.realpath(path)
dirwalk = lambda d: os.walk(d)
tree = lambda dir: concat(cmap(comp2(realpath)(jnpath(r)))(fs) for (r, ds, fs) in dirwalk(dir))


p = "D:/p4/wwe2k/main/Art/../Art/Characters20/" # realpath cleans up the ../Art bit

cmds.waitCursor(state=True)
t = tree(p)
l = list(t)
cmds.waitCursor(state=False)

cmds.window()
cmds.showWindow()
fl = cmds.formLayout()
tf = cmds.textField()
tsl = cmds.textScrollList()
ct = cmds.text()
cmds.formLayout(fl, edit=True, attachForm=[ (tf, "top", 0)
                                          , (tf, "left", 0)
                                          , (ct, "top", 0)
                                          , (ct, "right", 0)
                                          , (tsl, "left", 0)
                                          , (tsl, "right", 0)
                                          , (tsl, "bottom", 0)
                                          ]
                             , attachControl=[ (tsl, "top", 0, tf)
                                             , (tf, "right", 0, ct)
                                             ])


def repop (*_):
    pat = cmds.textField(tf, query=True, text=True)
    fs = [i for i in l if re.search(pat, i)]
    cmds.text(ct, edit=True, label=str(len(fs)) + "/" + str(len(l)))
    cmds.textScrollList(tsl, edit=True, removeAll=True, append=fs)
repop()

cmds.textField(tf, edit=True, textChangedCommand=repop)

