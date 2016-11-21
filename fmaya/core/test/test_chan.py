import unittest
from nose.plugins.attrib import attr

try:
    import maya.cmds as cmds
except ImportError:
    print 'WARNING (%s): failed to load maya.cmds module.' % __file__

from .. import chan


class Test_nodeFromChannel (unittest.TestCase):

    def test_nodeFromChannel_getsNodeFromNormalChannel (self):
        self.assertEquals(chan.nodeFromChannel("foo.bar"), "foo")

    def test_nodeFromChannel_doesNotAffectNonDottedName (self):
        self.assertEquals(chan.nodeFromChannel("foo"), "foo")

    def test_nodeFromChannel_handlesEmptyString (self):
        self.assertEquals(chan.nodeFromChannel(""), "")


class Test_attrFromChannel (unittest.TestCase):

    def test_attrFromChannel_getsAttrFromNormalChannel (self):
        self.assertEquals(chan.attrFromChannel("foo.bar"), "bar")

    def test_attrFromChannel_doesNotAffectNonDottedName (self):
        self.assertEquals(chan.attrFromChannel("bar"), "bar")


class Test_chanFromChannel (unittest.TestCase):

    def test_chanFromChannel_splitsAChannel (self):
        self.assertEquals(chan.chanFromChannel("foo.bar"), ("foo", "bar"))

    def test_chanFromChannel_emptyStringsFromEmptyString (self):
        self.assertEquals(chan.chanFromChannel(""), ("", ""))


class Test_attrToChannel (unittest.TestCase):

    def test_attrToChannel_createsChannel (self):
        self.assertEquals(chan.attrToChannel("foo")("bar"), "foo.bar")

    def test_attrToChannel_emptyNode (self):
        self.assertEquals(chan.attrToChannel("")("bar"), ".bar")

    def test_attrToChannel_emptyAttr (self):
        self.assertEquals(chan.attrToChannel("foo")(""), "foo.")

    def test_attrToChannel_emptyNodeAndAttr (self):
        self.assertEquals(chan.attrToChannel("")(""), ".")


class Test_minAndMax (unittest.TestCase):

    def test_minAndMax_raisesOnEmptyList (self):
        self.assertRaises(ValueError, lambda: chan.minAndMax([]))

    def test_minAndMax_findsOnlyElementInSingletonList (self):
        self.assertEquals(chan.minAndMax([3]), (3, 3))

    def test_minAndMax_findsMinAndMaxInLengthNList (self):
        self.assertEquals(chan.minAndMax([3,4,2,8,1,2,7]), (1, 8))

