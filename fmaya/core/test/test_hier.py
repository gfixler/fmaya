import unittest
from nose.plugins.attrib import attr

try:
    import maya.cmds as cmds
except ImportError:
    print 'WARNING (%s): failed to load maya.cmds module.' % __file__

from .. import hier


@attr('maya')
class Test_getParent (unittest.TestCase):

    def setUp (self):
        cmds.file(new=True, force=True)

    def test_getParent_returnsNoneOnRootObject (self):
        self.assertEquals(hier.getParent("persp"), None)

    def test_getParent_returnsParentIfOneExists (self):
        a = cmds.spaceLocator()[0]
        b = cmds.spaceLocator()[0]
        a2 = cmds.parent(a, b)
        self.assertEquals(hier.getParent(a2), b)

