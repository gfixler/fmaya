class UniqueWin (object):

    def __init__ (self, name, uiFunc=None, unique=True, autoCreate=True, **kwargs):
        """
        Creates a window that can recreate itself, first destroying a previous instance.

        uiFunc: a function that creates a UI, accepting the window name for parenting purposes
        name: string, required
        unique: bool, when win exists... True: destroy/remake, False: error out
        """
        self.name = "uw_" + name
        self.uiFunc = uiFunc
        self.unique = unique
        if autoCreate:
            self.create(**kwargs)

    def create (self, **kwargs):
        winName = toMayaName(self.name)
        if self.unique:
            if cmds.window(winName, query=True, exists=True):
                cmds.deleteUI(winName)
        self.win = cmds.window(winName)
        cmds.showWindow(**kwargs)
        if self.uiFunc:
            self.uiFunc(self.win)


"""
def myUI (parentUI):
    cmds.columnLayout(adjustableColumn=True, columnAttach=("both", 0))
    cmds.textField()
    cmds.button()

uw = UniqueWin("My Tool", myUI)
"""

