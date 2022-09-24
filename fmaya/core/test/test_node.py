import unittest
from nose.plugins.attrib import attr

import node

try:
    import maya.cmds as cmds
    hasMaya = True
except ImportError:
    print('WARNING (%s): failed to load maya.cmds module.' % __file__)
    hasMaya = False


@attr('maya')
@unittest.skipUnless(hasMaya, "requires Maya")
class Test_hasAttr (unittest.TestCase):

    def test_hasAttr_returnsFalseWhenAttrDoesNotExist (self):
        self.assertFalse(node.hasAttr("bloop")("persp"))

    def test_hasAttr_returnsTrueWhenAttrExists (self):
        self.assertTrue(node.hasAttr("ry")("persp"))

