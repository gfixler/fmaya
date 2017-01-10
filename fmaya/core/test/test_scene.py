import unittest
from nose.plugins.attrib import attr

try:
    import maya.cmds as cmds
except ImportError:
    print 'WARNING (%s): failed to load maya.cmds module.' % __file__

from .. import scene


# PURE

class Test_toValidMayaName (unittest.TestCase):

    def test_toValidMayaName_keepsValidName (self):
        self.assertEquals(scene.toValidMayaName("a_valid_name"), "a_valid_name")

    def test_toValidMayaName_keepsAnotherValidName (self):
        self.assertEquals(scene.toValidMayaName("ThisIsFine_too"), "ThisIsFine_too")

    def test_toValidMayaName_replacesDots (self):
        self.assertEquals(scene.toValidMayaName(".foo.bar.baz."), "_foo_bar_baz_")

    def test_toValidMayaName_replacesSpaces (self):
        self.assertEquals(scene.toValidMayaName(" foo bar baz "), "_foo_bar_baz_")

    def test_toValidMayaName_replacesPunctuation (self):
        self.assertEquals(scene.toValidMayaName("&foo*bar#baz%"), "_foo_bar_baz_")

    def test_toValidMayaName_replacesManyThings (self):
        self.assertEquals(scene.toValidMayaName("  This 'is' a test!"), "__This__is__a_test_")


# IMPURE

@attr('maya')
class Test_scenePath (unittest.TestCase):

    def setUp (self):
        cmds.file(new=True, force=True)

    def test_scenePath_getsScenePath (self):
        testPath = "/tmp/testMayaScene.ma"
        cmds.file(rename=testPath)
        self.assertEquals(scene.scenePath(), testPath)

    def test_sceneName_getsSceneName (self):
        testPath = "/tmp/testMayaScene.ma"
        testName = "testMayaScene.ma"
        cmds.file(rename=testPath)
        self.assertEquals(scene.sceneName(), testName)


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

