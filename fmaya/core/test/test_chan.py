import unittest
from nose.plugins.attrib import attr

try:
    import maya.cmds as cmds
except ImportError:
    print 'WARNING (%s): failed to load maya.cmds module.' % __file__

from .. import chan


# PURE

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


class Test_keysValueRange (unittest.TestCase):

    def test_keysValueRange_raisesOnEmptyList (self):
        self.assertRaises(ValueError, lambda: chan.keysValueRange([]))

    def test_keysValueRange_reportsProperRangeOnSingletonKeysList (self):
        self.assertEquals(chan.keysValueRange([(2,3)]), (3, 3))

    def test_keysValueRange_getsProperValueRange (self):
        self.assertEquals(chan.keysValueRange([(2,3),(4,2),(5,-1),(8,1)]), (-1, 3))


class Test_keysValueCenter (unittest.TestCase):

    def test_keysValueCenter_raisesOnEmptyList (self):
        self.assertRaises(ValueError, lambda: chan.keysValueCenter([]))

    def test_keysValueCenter_reportsProperRangeOnSingletonKeysList (self):
        self.assertEquals(chan.keysValueCenter([(2,3)]), 3)

    def test_keysValueCenter_getsProperValueCenter (self):
        self.assertEquals(chan.keysValueCenter([(2,3),(4,2),(5,-1),(8,1)]), 1)


# IMPURE

@attr('maya')
class Test_getTime (unittest.TestCase):

    def test_getTime_time0 (self):
        cmds.currentTime(5, edit=True)
        self.assertEquals(chan.getTime(), 5)

    def test_getTime_timeNegative20 (self):
        cmds.currentTime(-20, edit=True)
        self.assertEquals(chan.getTime(), -20)

    def test_getTime_time123 (self):
        cmds.currentTime(123, edit=True)
        self.assertEquals(chan.getTime(), 123)


@attr('maya')
class Test_getAttrType (unittest.TestCase):

    def test_getAttrType_translateX (self):
        self.assertEquals(chan.getAttrType('persp.translateX'), 'doubleLinear')

    def test_getAttrType_visibility (self):
        self.assertEquals(chan.getAttrType('persp.visibility'), 'bool')

