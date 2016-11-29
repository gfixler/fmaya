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

