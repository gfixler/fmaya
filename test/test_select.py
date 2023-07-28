import unittest
# from nose.plugins.attrib import attr

try:
    import maya.cmds as cmds
    hasMaya = True
except ImportError:
    # print('WARNING (%s): failed to load maya.cmds module.' % __file__)
    hasMaya = False

import select


# IMPURE

# @attr('maya')
@unittest.skipUnless(hasMaya, "requires Maya")
class Test_grab (unittest.TestCase):

    def test_grab_grabsNothing (self):
        cmds.select(None)
        select.grab()
        self.assertEqual(cmds.ls(selection=True), [])

    def test_grab_persp (self):
        select.grab("persp")
        self.assertEqual(cmds.ls(selection=True), ["persp"])

    def test_grab_andrelease (self):
        select.grab("persp")
        self.assertEqual(cmds.ls(selection=True), ["persp"])
        select.grab(None)
        self.assertEqual(cmds.ls(selection=True), [])

    def test_grab_changeGrabs (self):
        select.grab("persp")
        self.assertEqual(cmds.ls(selection=True), ["persp"])
        select.grab("side")
        self.assertEqual(cmds.ls(selection=True), ["side"])


# @attr('maya')
@unittest.skipUnless(hasMaya, "requires Maya")
class Test_selAndSelection1 (unittest.TestCase):

    def setUp (self):
        cmds.file(new=True, force=True)
        self.bs = list(map(lambda _: cmds.polySphere()[0], range(10)))
        self.cs = list(map(lambda _: cmds.polyCube()[0], range(10)))
        cmds.select(None)

    def test_sel_noSelectionYieldsEmptyList (self):
        self.assertEqual(select.sel(), [])

    def test_sel_getsSelection (self):
        bs = self.bs
        cs = self.cs
        xs = [bs[2], cs[1], bs[8], bs[5], cs[3]]
        cmds.select(xs)
        self.assertEqual(select.sel(), xs)

    def test_sel_getsAnotherSelection (self):
        cmds.select(self.bs)
        self.assertEqual(select.sel(), self.bs)

    def test_sel_sel1RaisesOnNoSelection (self):
        self.assertRaises(IndexError, select.sel1)

    def test_sel_sel1ReturnsOnlyItemSelected (self):
        cmds.select(self.bs[3])
        self.assertEqual(select.sel1(), self.bs[3])

    def test_sel_sel1ReturnsFirstItem (self):
        bs = self.bs
        cs = self.cs
        xs = [bs[2], cs[1], bs[8], bs[5], cs[3]]
        cmds.select(xs)
        self.assertEqual(select.sel1(), xs[0])


# @attr('maya')
class Test_channelBoxSelection (unittest.TestCase):

    # this relies on the GUI, and is therefore untestable
    pass

