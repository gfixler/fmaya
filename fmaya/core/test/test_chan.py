import unittest
from nose.plugins.attrib import attr

try:
    import maya.cmds as cmds
except ImportError:
    print 'WARNING (%s): failed to load maya.cmds module.' % __file__

from .. import chan

class Test_pureChannelStringFunctions (unittest.TestCase):

    def test_nodeFromChannel_getsNodeFromNormalChannel (self):
        self.assertEquals(chan.nodeFromChannel("foo.bar"), "foo")

    def test_nodeFromChannel_doesNotAffectNonDottedName (self):
        self.assertEquals(chan.nodeFromChannel("foo"), "foo")

    def test_nodeFromChannel_handlesEmptyString (self):
        self.assertEquals(chan.nodeFromChannel(""), "")

    def test_attrFromChannel_getsAttrFromNormalChannel (self):
        self.assertEquals(chan.attrFromChannel("foo.bar"), "bar")

    def test_attrFromChannel_doesNotAffectNonDottedName (self):
        self.assertEquals(chan.attrFromChannel("bar"), "bar")

    def test_chanFromChannel_splitsAChannel (self):
        self.assertEquals(chan.chanFromChannel("foo.bar"), ("foo", "bar"))

    def test_chanFromChannel_emptyStringsFromEmptyString (self):
        self.assertEquals(chan.chanFromChannel(""), ("", ""))

