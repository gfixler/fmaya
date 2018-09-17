import unittest
from nose.plugins.attrib import attr

try:
    import maya.cmds as cmds
except ImportError:
    print 'WARNING (%s): failed to load maya.cmds module.' % __file__

from .. import scene

import os
import tempfile

# IMPURE

@attr('maya')
class Test_scenePath (unittest.TestCase):

    def test_scenePath_getsScenePath (self):
        tf = tempfile.TemporaryFile(suffix='.ma')
        tfn = os.path.normpath(tf.name)
        tfn = os.path.normpath(tfn)
        cmds.file(rename=tfn)
        sp = scene.scenePath()
        spn = os.path.normpath(sp)
        self.assertEquals(spn, tfn)


@attr('maya')
class Test_sceneName (unittest.TestCase):

    def test_scenePath_getsSceneName (self):
        tf = tempfile.TemporaryFile(suffix='.ma')
        cmds.file(rename=tf.name)
        name = os.path.basename(tf.name)
        self.assertEquals(scene.sceneName(), name)


@attr('maya')
class Test_grepScene (unittest.TestCase):

    def setUp (self):
        cmds.file(new=True, force=True)

    def test_grepScene_emptyPatternFindsAllObjects (self):
        self.assertEquals(scene.grepScene(""), cmds.ls(allPaths=True))

    def test_grepScene_findsCameras (self):
        self.assertEquals(set(scene.grepScene("Shape$")), set(["perspShape","topShape","frontShape","sideShape"]))

    def test_grepScene_findsDefaultGlobals (self):
        expected = ["defaultRenderGlobals","defaultHardwareRenderGlobals","defaultColorMgtGlobals"]
        self.assertEquals(set(scene.grepScene("^default.*Globals$")), set(expected))

    def test_grepScene_findsNumericPatterns (self):
        for i in xrange(20):
            cmds.spaceLocator(name="loc{0:b}".format(i))
        expected = ["loc101", "loc1111", "loc1101", "loc111"]
        self.assertEquals(set(scene.grepScene("1[01]1$")), set(expected))

    def test_grepScene_findsNamesWithNoCapitalLetters (self):
        self.assertEquals(set(scene.grepScene("^[a-z]+$")), set(["front","persp","top","side"]))

    def test_grepScene_findsASpecificPattern (self):
        self.assertEquals(set(scene.grepScene("e......s")), set(["strokeGlobals", "defaultRenderingList1"]))


@attr('maya')
class Test_obExists (unittest.TestCase):

    def setUp (self):
        cmds.file(new=True, force=True)

    def test_obExists_falseOnNonExistence (self):
        self.assertFalse(scene.obExists("thisDoesNotExist"))

    def test_obExists_trueOnExistence (self):
        self.assertTrue(scene.obExists("persp"))


@attr('maya')
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


@attr('maya')
class Test_lsNamespaces (unittest.TestCase):

    def setUp (self):
        cmds.file(new=True, force=True)

    def test_lsNamespaces_findsDefaults (self):
        self.assertEquals(set(scene.lsNamespaces()), set([":","UI","shared"]))

    def test_lsNamespaces_findsUserCreated (self):
        cmds.namespace(add="foo:bar")
        cmds.namespace(add="baz")
        self.assertEquals(set(scene.lsNamespaces()), set([":","UI","shared","foo","foo:bar","baz"]))


@attr('maya')
class Test_lsNamespacesContaining (unittest.TestCase):

    def setUp (self):
        cmds.file(new=True, force=True)

    def test_lsNamespacesContaining_findsPerspInDefaultSceneRoot (self):
        self.assertEquals(set(scene.lsNamespacesContaining("persp")), set([":"]))

    def test_lsNamespacesContaining_findsObjectNamespaceAmongMany (self):
        cmds.namespace(add="foo:bar")
        cmds.namespace(add="baz")
        cmds.namespace(set="foo")
        cmds.spaceLocator(name="Waldo")
        cmds.namespace(set=":")
        self.assertEquals(scene.lsNamespacesContaining("Waldo"), [":", "foo"])


@attr('maya')
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


@attr('maya')
class Test_atTime_ (unittest.TestCase):

    def test_atTime__readsTimeAtIntTime (self):
        self.assertEquals(scene.atTime_(37)(lambda: cmds.currentTime(query=True)), 37)

    def test_atTime__readsTimeAtFloatTime (self):
        self.assertAlmostEquals(scene.atTime_(13.7)(lambda: cmds.currentTime(query=True)), 13.7)


@attr('maya')
class Test_atFrame (unittest.TestCase):

    def setUp (self):
        self.loc = cmds.spaceLocator()[0]
        self.testAttr = self.loc + ".ty"

        cmds.setKeyframe(self.testAttr, time=0, value=0)
        cmds.setKeyframe(self.testAttr, time=10, value=5)

    def test_atFrame_readsValueAtNearestFrame (self):
        self.assertAlmostEquals(scene.atFrame(9.51)(cmds.getAttr)(self.testAttr), 5)


@attr('maya')
class Test_atFrame_ (unittest.TestCase):

    def test_atFrame__readsFrameAtIntTime (self):
        self.assertEquals(scene.atFrame_(37)(lambda: cmds.currentTime(query=True)), 37)

    def test_atFrame__readsFrameAtFloatTime (self):
        self.assertEquals(scene.atFrame_(13.7)(lambda: cmds.currentTime(query=True)), 14)


@attr('maya')
class Test_inTime (unittest.TestCase):

    def setUp (self):
        cmds.file(new=True, force=True)

    def test_inTime_getsFrame1FromNewScene (self):
        self.assertEquals(scene.inTime(), 1.0)

    def test_inTime_getsIntFirstFrameTime (self):
        cmds.playbackOptions(edit=True, minTime=37)
        self.assertEquals(scene.inTime(), 37.0)

    def test_inTime_getsFloatFirstFrameTime (self):
        cmds.playbackOptions(edit=True, minTime=13.23)
        self.assertEquals(scene.inTime(), 13.23)


@attr('maya')
class Test_outTime (unittest.TestCase):

    def setUp (self):
        cmds.file(new=True, force=True)

    def test_outTime_getsFrame120FromNewScene (self):
        self.assertEquals(scene.outTime(), 120.0)

    def test_outTime_getsIntLastFrameTime (self):
        cmds.playbackOptions(edit=True, maxTime=234.0)
        self.assertEquals(scene.outTime(), 234.0)

    def test_outTime_getsFloatLastFrameTime (self):
        cmds.playbackOptions(edit=True, maxTime=17.3)
        self.assertEquals(scene.outTime(), 17.3)

