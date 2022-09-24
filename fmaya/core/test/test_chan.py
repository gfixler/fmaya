import unittest
from nose.plugins.attrib import attr

try:
    import maya.cmds as cmds
except ImportError:
    print 'WARNING (%s): failed to load maya.cmds module.' % __file__

import chan


# PURE

class Test_nodeFromChannel (unittest.TestCase):

    def test_nodeFromChannel_getsNodeFromNormalChannel (self):
        self.assertEqual(chan.nodeFromChannel("foo.bar"), "foo")

    def test_nodeFromChannel_doesNotAffectNonDottedName (self):
        self.assertEqual(chan.nodeFromChannel("foo"), "foo")

    def test_nodeFromChannel_handlesEmptyString (self):
        self.assertEqual(chan.nodeFromChannel(""), "")


class Test_attrFromChannel (unittest.TestCase):

    def test_attrFromChannel_getsAttrFromNormalChannel (self):
        self.assertEqual(chan.attrFromChannel("foo.bar"), "bar")

    def test_attrFromChannel_doesNotAffectNonDottedName (self):
        self.assertEqual(chan.attrFromChannel("bar"), "bar")


class Test_chanFromChannel (unittest.TestCase):

    def test_chanFromChannel_splitsAChannel (self):
        self.assertEqual(chan.chanFromChannel("foo.bar"), ("foo", "bar"))

    def test_chanFromChannel_emptyStringsFromEmptyString (self):
        self.assertEqual(chan.chanFromChannel(""), ("", ""))


class Test_attrToChannel (unittest.TestCase):

    def test_attrToChannel_createsChannel (self):
        self.assertEqual(chan.attrToChannel("foo")("bar"), "foo.bar")

    def test_attrToChannel_emptyNode (self):
        self.assertEqual(chan.attrToChannel("")("bar"), ".bar")

    def test_attrToChannel_emptyAttr (self):
        self.assertEqual(chan.attrToChannel("foo")(""), "foo.")

    def test_attrToChannel_emptyNodeAndAttr (self):
        self.assertEqual(chan.attrToChannel("")(""), ".")


class Test_keysValueRange (unittest.TestCase):

    def test_keysValueRange_raisesOnEmptyList (self):
        self.assertRaises(ValueError, lambda: chan.keysValueRange([]))

    def test_keysValueRange_reportsProperRangeOnSingletonKeysList (self):
        self.assertEqual(chan.keysValueRange([(2,3)]), (3, 3))

    def test_keysValueRange_getsProperValueRange (self):
        self.assertEqual(chan.keysValueRange([(2,3),(4,2),(5,-1),(8,1)]), (-1, 3))


class Test_keysValueCenter (unittest.TestCase):

    def test_keysValueCenter_raisesOnEmptyList (self):
        self.assertRaises(ValueError, lambda: chan.keysValueCenter([]))

    def test_keysValueCenter_reportsProperRangeOnSingletonKeysList (self):
        self.assertEqual(chan.keysValueCenter([(2,3)]), 3)

    def test_keysValueCenter_getsProperValueCenter (self):
        self.assertEqual(chan.keysValueCenter([(2,3),(4,2),(5,-1),(8,1)]), 1)


# IMPURE

@attr('maya')
class Test_getChanType (unittest.TestCase):

    def test_getAttrType_translateX (self):
        self.assertEqual(chan.getChannelType('persp.translateX'), 'doubleLinear')

    def test_getAttrType_visibility (self):
        self.assertEqual(chan.getChannelType('persp.visibility'), 'bool')


@attr('maya')
class Test_getChannelAtTime (unittest.TestCase):

    def setUp (self):
        cmds.file(new=True, force=True)
        cmds.setKeyframe('persp.tx', time=-3, value=7)
        cmds.setKeyframe('persp.tx', time=8, value=13)

    def test_getChannelAtTime_getsValueOfUnkeyedChannel (self):
        cmds.setAttr('persp.rz', 23)
        self.assertEqual(chan.getChannelAtTime(-4)('persp.rz'), 23)
        self.assertEqual(chan.getChannelAtTime(0)('persp.rz'), 23)
        self.assertEqual(chan.getChannelAtTime(17)('persp.rz'), 23)

    def test_getChannelAtTime_getsValueAtKey (self):
        self.assertEqual(chan.getChannelAtTime(-3)('persp.tx'), 7)

    def test_getChannelAtTime_getsValueAtAnotherKey (self):
        self.assertEqual(chan.getChannelAtTime(8)('persp.tx'), 13)


@attr('maya')
class Test_setChannel (unittest.TestCase):

    def setUp (self):
        cmds.file(new=True, force=True)
        cmds.setKeyframe('persp.tx', time=-3, value=7)
        cmds.setKeyframe('persp.tx', time=8, value=13)

    def test_setChannel_setsValuesAtTimes (self):
        chan.setChannel("persp.rz")((5,23))
        chan.setChannel("persp.rz")((7,-3))
        chan.setChannel("persp.rz")((2,13))
        cmds.currentTime(2, edit=True)
        self.assertAlmostEquals(cmds.getAttr("persp.rz"), 13)
        cmds.currentTime(5, edit=True)
        self.assertAlmostEquals(cmds.getAttr("persp.rz"), 23)
        cmds.currentTime(7, edit=True)
        self.assertAlmostEquals(cmds.getAttr("persp.rz"), -3)


@attr('maya')
class Test_getAttr (unittest.TestCase):

    def setUp (self):
        self.loc = cmds.spaceLocator()[0]
        cmds.setAttr(self.loc + ".ty", -23.0)
        cmds.setAttr(self.loc + ".tz", 7.5)
        cmds.setAttr(self.loc + ".ry", 123.0)
        cmds.setAttr(self.loc + ".rz", -220.0)

    def test_getAttr_getsAnAttr (self):
        self.assertEqual(chan.getAttr("ty")(self.loc), -23.0)


@attr('maya')
class Test_modAttr (unittest.TestCase):

    def setUp (self):
        self.loc = cmds.spaceLocator()[0]

    def tests_modAttr_identity (self):
        chan.modAttr("sy")(lambda x: x)(self.loc)
        self.assertEqual(cmds.getAttr(self.loc + ".sy"), 1.0)

    def test_modAttr_modsAndAttrWithAddition (self):
        chan.modAttr("ty")(lambda y: y + 3)(self.loc)
        self.assertEqual(cmds.getAttr(self.loc + ".ty"), 3.0)

    def tests_modAttr_modsAnAttrWithMultiplication (self):
        chan.modAttr("sz")(lambda z: z * 4)(self.loc)
        self.assertEqual(cmds.getAttr(self.loc + ".sz"), 4.0)


@attr('maya')
class Test_setAttr (unittest.TestCase):

    def setUp (self):
        self.loc = cmds.spaceLocator()[0]

    def test_setAttr_setsAnAttr (self):
        chan.setAttr("ty")(37.0)(self.loc)
        self.assertEqual(cmds.getAttr(self.loc + ".ty"), 37.0)


@attr('maya')
class Test_getKeyTimesAndValuesAndKeys (unittest.TestCase):

    def setUp (self):
        cmds.file(new=True, force=True)
        cmds.setKeyframe('persp.tx', time=-3, value=100)
        cmds.setKeyframe('persp.tx', time=0, value=-56)
        cmds.setKeyframe('persp.tx', time=5, value=33)

    def test_getKeyTimes_getsKeys (self):
        self.assertEqual(chan.getKeyTimes('persp.tx'), [-3,0,5])

    def test_getKeyValues_getsValues (self):
        self.assertEqual(chan.getKeyValues('persp.tx'), [100,-56,33])

    def test_getKeys_getsKeys (self):
        self.assertEqual(chan.getKeys('persp.tx'), [(-3,100),(0,-56),(5,33)])


@attr('maya')
class Test_hasKeys (unittest.TestCase):

    def setUp (self):
        cmds.file(new=True, force=True)
        cmds.setKeyframe('persp.tx', time=-3, value=100)
        cmds.setKeyframe('persp.tx', time=0, value=-56)
        cmds.setKeyframe('persp.tx', time=5, value=33)

    def test_hasKeys_keyedCameraHasKeys (self):
        self.assertTrue(chan.hasKeys("persp"))

    def test_hasKeys_unkeyedCameraHasNoKeys (self):
        self.assertFalse(chan.hasKeys("side"))


@attr('maya')
class Test_artistAttrs (unittest.TestCase):

    def setUp (self):
        cmds.file(new=True, force=True)

        self.cube = cmds.polyCube()[0]

        self.ball = cmds.polySphere()[0]
        cmds.setAttr(self.ball + ".tz", lock=True)
        cmds.setAttr(self.ball + ".sx", keyable=False)
        cmds.addAttr(self.ball, longName="foo", keyable=True, hidden=True)
        cmds.addAttr(self.ball, longName="bar", keyable=True)

        self.loc = cmds.spaceLocator()[0]
        for attr in ["tx","ty","tz","rx","ry","rz","sx","sy","sz","v"]:
            cmds.setAttr(self.loc + "." + attr, keyable=False)

    def test_artistAttrs_findsDefaultChannels (self):
        expected = [ "translateX"
                   , "translateY"
                   , "translateZ"
                   , "rotateX"
                   , "rotateY"
                   , "rotateZ"
                   , "scaleX"
                   , "scaleY"
                   , "scaleZ"
                   , "visibility"
                   ]
        self.assertEqual(sorted(chan.artistAttrs(self.cube)), sorted(expected))

    def test_artistAttrs_doesNotFindHiddenLockedOrNonKeyableChannels (self):
        expected = [ "translateX"
                   , "translateY"
                   , "rotateX"
                   , "rotateY"
                   , "rotateZ"
                   , "scaleY"
                   , "scaleZ"
                   , "visibility"
                   , "bar"
                   ]
        self.assertEqual(sorted(chan.artistAttrs(self.ball)), sorted(expected))

    def test_artistAttrs_returnsEmptyListWhenAllChannelsNonKeyable (self):
        self.assertEqual(chan.artistAttrs(self.loc), [])


@attr('maya')
class Test_artistChannels (unittest.TestCase):

    def setUp (self):
        cmds.file(new=True, force=True)

        self.cube = cmds.polyCube()[0]

        self.ball = cmds.polySphere()[0]
        cmds.setAttr(self.ball + ".tz", lock=True)
        cmds.setAttr(self.ball + ".sx", keyable=False)
        cmds.addAttr(self.ball, longName="foo", keyable=True, hidden=True)
        cmds.addAttr(self.ball, longName="bar", keyable=True)

        self.loc = cmds.spaceLocator()[0]
        for attr in ["tx","ty","tz","rx","ry","rz","sx","sy","sz","v"]:
            cmds.setAttr(self.loc + "." + attr, keyable=False)

    def test_artistChannels_findsDefaultChannels (self):
        expected = [ self.cube + ".translateX"
                   , self.cube + ".translateY"
                   , self.cube + ".translateZ"
                   , self.cube + ".rotateX"
                   , self.cube + ".rotateY"
                   , self.cube + ".rotateZ"
                   , self.cube + ".scaleX"
                   , self.cube + ".scaleY"
                   , self.cube + ".scaleZ"
                   , self.cube + ".visibility"
                   ]
        self.assertEqual(sorted(chan.artistChannels(self.cube)), sorted(expected))

    def test_artistChannels_doesNotFindHiddenLockedOrNonKeyableChannels (self):
        expected = [ self.ball + ".translateX"
                   , self.ball + ".translateY"
                   , self.ball + ".rotateX"
                   , self.ball + ".rotateY"
                   , self.ball + ".rotateZ"
                   , self.ball + ".scaleY"
                   , self.ball + ".scaleZ"
                   , self.ball + ".visibility"
                   , self.ball + ".bar"
                   ]
        self.assertEqual(sorted(chan.artistChannels(self.ball)), sorted(expected))

    def test_artistChannels_returnsEmptyListWhenAllChannelsNonKeyable (self):
        self.assertEqual(chan.artistChannels(self.loc), [])


@attr('maya')
class Test_isNumericChannel (unittest.TestCase):

    def test_isNumericChannel_nonNumericChannelYieldsFalse (self):
        self.assertEqual(chan.isNumericChannel('persp.visibility'), False)

    def test_isNumericChannel_numericChannelYieldsTrue (self):
        self.assertEqual(chan.isNumericChannel('persp.rx'), True)


@attr('maya')
class Test_numericArtistChannels (unittest.TestCase):

    def setUp (self):
        cmds.file(new=True, force=True)

        self.cube = cmds.polyCube()[0]

        self.ball = cmds.polySphere()[0]
        cmds.setAttr(self.ball + ".tz", lock=True)
        cmds.setAttr(self.ball + ".sx", keyable=False)
        cmds.addAttr(self.ball, longName="foo", keyable=True, hidden=True)
        cmds.addAttr(self.ball, longName="bar", keyable=True, attributeType="matrix")
        cmds.addAttr(self.ball, longName="baz", keyable=True)

        self.loc = cmds.spaceLocator()[0]
        for attr in ["tx","ty","tz","rx","ry","rz","sx","sy","sz","v"]:
            cmds.setAttr(self.loc + "." + attr, keyable=False)

    def test_numericArtistChannels_findsDefaultChannels (self):
        expected = [ self.cube + ".translateX"
                   , self.cube + ".translateY"
                   , self.cube + ".translateZ"
                   , self.cube + ".rotateX"
                   , self.cube + ".rotateY"
                   , self.cube + ".rotateZ"
                   , self.cube + ".scaleX"
                   , self.cube + ".scaleY"
                   , self.cube + ".scaleZ"
                   ]
        self.assertEqual(sorted(chan.numericArtistChannels(self.cube)), sorted(expected))

    def test_numericArtistChannels_doesNotFindHiddenLockedOrNonKeyableChannels (self):
        expected = [ self.ball + ".translateX"
                   , self.ball + ".translateY"
                   , self.ball + ".rotateX"
                   , self.ball + ".rotateY"
                   , self.ball + ".rotateZ"
                   , self.ball + ".scaleY"
                   , self.ball + ".scaleZ"
                   , self.ball + ".baz"
                   ]
        self.assertEqual(sorted(chan.numericArtistChannels(self.ball)), sorted(expected))

    def test_artistChannels_returnsEmptyListWhenAllChannelsNonKeyable (self):
        self.assertEqual(chan.numericArtistChannels(self.loc), [])

