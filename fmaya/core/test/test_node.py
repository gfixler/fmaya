import unittest
from nose.plugins.attrib import attr

from .. import node


@attr('maya')
class Test_hasAttr (unittest.TestCase):

    def test_hasAttr_returnsFalseWhenAttrDoesNotExist (self):
        self.assertFalse(node.hasAttr("bloop")("persp"))

    def test_hasAttr_returnsTrueWhenAttrExists (self):
        self.assertTrue(node.hasAttr("ry")("persp"))

