import unittest
# from nose.plugins.attrib import attr

try:
    import maya.cmds as cmds
    hasMaya = True
except ImportError:
    # print('WARNING (%s): failed to load maya.cmds module.' % __file__)
    hasMaya = False

import scene

import os
import tempfile


# IMPURE

# @attr('maya')
@unittest.skipUnless(hasMaya, "requires Maya")
class Test_scenePath (unittest.TestCase):

    def test_scenePath_getsScenePath (self):
        tf = tempfile.TemporaryFile(suffix='.ma')
        tfn = os.path.normpath(tf.name)
        tfn = os.path.normpath(tfn)
        cmds.file(rename=tfn)
        sp = scene.scenePath()
        spn = os.path.normpath(sp)
        self.assertEqual(spn, tfn)


# @attr('maya')
@unittest.skipUnless(hasMaya, "requires Maya")
class Test_sceneName (unittest.TestCase):

    def test_scenePath_getsSceneName (self):
        tf = tempfile.TemporaryFile(suffix='.ma')
        cmds.file(rename=tf.name)
        name = os.path.basename(tf.name)
        self.assertEqual(scene.sceneName(), name)


# @attr('maya')
@unittest.skipUnless(hasMaya, "requires Maya")
class Test_grepScene (unittest.TestCase):

    def setUp (self):
        cmds.file(new=True, force=True)

    def test_grepScene_emptyPatternFindsAllObjects (self):
        self.assertEqual(scene.grepScene(""), cmds.ls(allPaths=True))

    def test_grepScene_findsCameras (self):
        self.assertEqual(set(scene.grepScene("Shape$")), set(["perspShape","topShape","frontShape","sideShape"]))

    def test_grepScene_findsDefaultGlobals (self):
        expected = ["defaultRenderGlobals","defaultHardwareRenderGlobals","defaultColorMgtGlobals"]
        self.assertEqual(set(scene.grepScene("^default.*Globals$")), set(expected))

    def test_grepScene_findsNumericPatterns (self):
        for i in xrange(20):
            cmds.spaceLocator(name="loc{0:b}".format(i))
        expected = ["loc101", "loc1111", "loc1101", "loc111"]
        self.assertEqual(set(scene.grepScene("1[01]1$")), set(expected))

    def test_grepScene_findsNamesWithNoCapitalLetters (self):
        self.assertEqual(set(scene.grepScene("^[a-z]+$")), set(["front","persp","top","side"]))

    def test_grepScene_findsASpecificPattern (self):
        self.assertEqual(set(scene.grepScene("e......s")), set(["strokeGlobals", "defaultRenderingList1"]))


# @attr('maya')
@unittest.skipUnless(hasMaya, "requires Maya")
class Test_getTime (unittest.TestCase):

    def test_getTime_time0 (self):
        cmds.currentTime(5, edit=True)
        self.assertEqual(scene.getTime(), 5)

    def test_getTime_timeNegative20 (self):
        cmds.currentTime(-20, edit=True)
        self.assertEqual(scene.getTime(), -20)

    def test_getTime_time123 (self):
        cmds.currentTime(123, edit=True)
        self.assertEqual(scene.getTime(), 123)


# @attr('maya')
@unittest.skipUnless(hasMaya, "requires Maya")
class Test_obExists (unittest.TestCase):

    def setUp (self):
        cmds.file(new=True, force=True)

    def test_obExists_falseOnNonExistence (self):
        self.assertFalse(scene.obExists("thisDoesNotExist"))

    def test_obExists_trueOnExistence (self):
        self.assertTrue(scene.obExists("persp"))


# @attr('maya')
@unittest.skipUnless(hasMaya, "requires Maya")
class Test_inNS (unittest.TestCase):

    def setUp (self):
        cmds.file(new=True, force=True)
        cmds.namespace(add=":foo:bar")

    def test_inNS_doesNotFindThingNotInNamespace (self):
        self.assertFalse(scene.inNS("foo:bar")("persp"))

    def test_inNS_findsThingInNamespace (self):
        cmds.namespace(set=":foo:bar")
        loc = cmds.spaceLocator()[0]
        self.assertFalse(scene.inNS("foo:bar")(loc))


# @attr('maya')
@unittest.skipUnless(hasMaya, "requires Maya")
class Test_lsNamespaces (unittest.TestCase):

    def setUp (self):
        cmds.file(new=True, force=True)

    def test_lsNamespaces_findsDefaults (self):
        self.assertEqual(set(scene.lsNamespaces()), set([":","UI","shared"]))

    def test_lsNamespaces_findsUserCreated (self):
        cmds.namespace(add="foo:bar")
        cmds.namespace(add="baz")
        self.assertEqual(set(scene.lsNamespaces()), set([":","UI","shared","foo","foo:bar","baz"]))


# @attr('maya')
@unittest.skipUnless(hasMaya, "requires Maya")
class Test_lsNamespacesContaining (unittest.TestCase):

    def setUp (self):
        cmds.file(new=True, force=True)

    def test_lsNamespacesContaining_findsPerspInDefaultSceneRoot (self):
        self.assertEqual(set(scene.lsNamespacesContaining("persp")), set([":"]))

    def test_lsNamespacesContaining_findsObjectNamespaceAmongMany (self):
        cmds.namespace(add="foo:bar")
        cmds.namespace(add="baz")
        cmds.namespace(set="foo")
        cmds.spaceLocator(name="Waldo")
        cmds.namespace(set=":")
        self.assertEqual(scene.lsNamespacesContaining("Waldo"), [":", "foo"])


# @attr('maya')
@unittest.skipUnless(hasMaya, "requires Maya")
class Test_atTime (unittest.TestCase):

    def setUp (self):
        self.loc = cmds.spaceLocator()[0]
        self.testAttr = self.loc + ".ty"

        cmds.setKeyframe(self.testAttr, time=0, value=0)
        cmds.setKeyframe(self.testAttr, time=10, value=5)

    def test_atTime_readsKeyedValueAtIntTime (self):
        self.assertAlmostEquals(scene.atTime(5)(cmds.getAttr)(self.testAttr), 2.5)

    def test_atTime_readsKeyedValueAtFloatTime (self):
        self.assertAlmostEquals(scene.atTime(7.5)(cmds.getAttr)(self.testAttr), 3.75)


# @attr('maya')
@unittest.skipUnless(hasMaya, "requires Maya")
class Test_atTime_ (unittest.TestCase):

    def test_atTime__readsTimeAtIntTime (self):
        self.assertEqual(scene.atTime_(37)(lambda: cmds.currentTime(query=True)), 37)

    def test_atTime__readsTimeAtFloatTime (self):
        self.assertAlmostEquals(scene.atTime_(13.7)(lambda: cmds.currentTime(query=True)), 13.7)


# @attr('maya')
@unittest.skipUnless(hasMaya, "requires Maya")
class Test_atFrame (unittest.TestCase):

    def setUp (self):
        self.loc = cmds.spaceLocator()[0]
        self.testAttr = self.loc + ".ty"

        cmds.setKeyframe(self.testAttr, time=0, value=0)
        cmds.setKeyframe(self.testAttr, time=10, value=5)

    def test_atFrame_readsValueAtNearestFrame (self):
        self.assertAlmostEquals(scene.atFrame(9.51)(cmds.getAttr)(self.testAttr), 5)


# @attr('maya')
@unittest.skipUnless(hasMaya, "requires Maya")
class Test_atFrame_ (unittest.TestCase):

    def test_atFrame__readsFrameAtIntTime (self):
        self.assertEqual(scene.atFrame_(37)(lambda: cmds.currentTime(query=True)), 37)

    def test_atFrame__readsFrameAtFloatTime (self):
        self.assertEqual(scene.atFrame_(13.7)(lambda: cmds.currentTime(query=True)), 14)


# @attr('maya')
@unittest.skipUnless(hasMaya, "requires Maya")
class Test_inTime (unittest.TestCase):

    def setUp (self):
        cmds.file(new=True, force=True)

    def test_inTime_getsFrame1FromNewScene (self):
        self.assertEqual(scene.inTime(), 1.0)

    def test_inTime_getsIntFirstFrameTime (self):
        cmds.playbackOptions(edit=True, minTime=37)
        self.assertEqual(scene.inTime(), 37.0)

    def test_inTime_getsFloatFirstFrameTime (self):
        cmds.playbackOptions(edit=True, minTime=13.23)
        self.assertEqual(scene.inTime(), 13.23)


# @attr('maya')
@unittest.skipUnless(hasMaya, "requires Maya")
class Test_outTime (unittest.TestCase):

    def setUp (self):
        cmds.file(new=True, force=True)

    def test_outTime_getsFrame120FromNewScene (self):
        self.assertEqual(scene.outTime(), 120.0)

    def test_outTime_getsIntLastFrameTime (self):
        cmds.playbackOptions(edit=True, maxTime=234.0)
        self.assertEqual(scene.outTime(), 234.0)

    def test_outTime_getsFloatLastFrameTime (self):
        cmds.playbackOptions(edit=True, maxTime=17.3)
        self.assertEqual(scene.outTime(), 17.3)


# @attr('maya')
@unittest.skipUnless(hasMaya, "requires Maya")
class Test_inFrame (unittest.TestCase):

    def setUp (self):
        cmds.file(new=True, force=True)

    def test_inFrame_getIntInFrame (self):
        cmds.playbackOptions(edit=True, minTime=23.0)
        self.assertEqual(scene.inFrame(), 23.0)

    def test_inFrame_getFloatInFrame (self):
        cmds.playbackOptions(edit=True, minTime=29.6)
        self.assertEqual(scene.inFrame(), 30.0)


# @attr('maya')
@unittest.skipUnless(hasMaya, "requires Maya")
class Test_outFrame (unittest.TestCase):

    def setUp (self):
        cmds.file(new=True, force=True)

    def test_outFrame_getIntOutFrame (self):
        cmds.playbackOptions(edit=True, maxTime=180.0)
        self.assertEqual(scene.outFrame(), 180.0)

    def test_outFrame_getFloatOutFrame (self):
        cmds.playbackOptions(edit=True, maxTime=221.3)
        self.assertEqual(scene.outFrame(), 221.0)


# @attr('maya')
@unittest.skipUnless(hasMaya, "requires Maya")
class Test_allFrames (unittest.TestCase):

    def setUp (self):
        cmds.file(new=True, force=True)

    def test_allFrames_defaultsTo1To120 (self):
        self.assertEqual(list(scene.allFrames()), list(xrange(1, 120)))

    def test_allFrames_getsSetIntRange (self):
        cmds.playbackOptions(edit=True, minTime=23.0)
        cmds.playbackOptions(edit=True, maxTime=67.0)
        self.assertEqual(list(scene.allFrames()), list(xrange(23, 67)))

    def test_allFrames_getsSetFloatRange (self):
        cmds.playbackOptions(edit=True, minTime=23.7)
        cmds.playbackOptions(edit=True, maxTime=67.6)
        self.assertEqual(list(scene.allFrames()), list(xrange(24, 68)))

