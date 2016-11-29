import unittest
from nose.plugins.attrib import attr

try:
    import maya.cmds as cmds
except ImportError:
    print 'WARNING (%s): failed to load maya.cmds module.' % __file__

from .. import select


@attr('maya')
class Test_selectionAndSelection1 (unittest.TestCase):

    def setUp (self):
        cmds.file(new=True, force=True)
        self.bs = map(lambda _: cmds.polySphere()[0], xrange(10))
        self.cs = map(lambda _: cmds.polyCube()[0], xrange(10))
        cmds.select(None)

    def test_selection_noSelectionYieldsEmptyList (self):
        self.assertEquals(select.selection(), [])

    def test_selection_getsSelection (self):
        bs = self.bs
        cs = self.cs
        xs = [bs[2], cs[1], bs[8], bs[5], cs[3]]
        cmds.select(xs)
        self.assertEquals(select.selection(), xs)

    def test_selection_getsAnotherSelection (self):
        cmds.select(self.bs)
        self.assertEquals(select.selection(), self.bs)

    def test_selection_selection1RaisesOnNoSelection (self):
        self.assertRaises(IndexError, select.selection1)

    def test_selection_selection1ReturnsOnlyItemSelected (self):
        cmds.select(self.bs[3])
        self.assertEquals(select.selection1(), self.bs[3])

    def test_selection_selection1ReturnsFirstItem (self):
        bs = self.bs
        cs = self.cs
        xs = [bs[2], cs[1], bs[8], bs[5], cs[3]]
        cmds.select(xs)
        self.assertEquals(select.selection1(), xs[0])

