import unittest
# from nose.plugins.attrib import attr

import maya.standalone
maya.standalone.initialize(name="python")

try:
    import maya.cmds as cmds
    hasMaya = True
except ImportError:
    # print('WARNING (%s): failed to load maya.cmds module.' % __file__)
    hasMaya = False

import name


class Test_toValidMayaName (unittest.TestCase):

    def test_toValidMayaName_keepsValidName (self):
        self.assertEqual(name.toValidMayaName("a_valid_name"), "a_valid_name")

    def test_toValidMayaName_keepsAnotherValidName (self):
        self.assertEqual(name.toValidMayaName("ThisIsFine_too"), "ThisIsFine_too")

    def test_toValidMayaName_replacesDots (self):
        self.assertEqual(name.toValidMayaName(".foo.bar.baz."), "_foo_bar_baz_")

    def test_toValidMayaName_replacesSpaces (self):
        self.assertEqual(name.toValidMayaName(" foo bar baz "), "_foo_bar_baz_")

    def test_toValidMayaName_replacesPunctuation (self):
        self.assertEqual(name.toValidMayaName("&foo*bar#baz%"), "_foo_bar_baz_")

    def test_toValidMayaName_replacesManyThings (self):
        self.assertEqual(name.toValidMayaName("  This 'is' a test!"), "__This__is__a_test_")


class Test_withNS (unittest.TestCase):

    def test_withNS_prependsColonWhenNSIsEmptyString (self):
        self.assertEqual(name.withNS("")("foo"), ":foo")

    def test_withNS_joinsAroundColon (self):
        self.assertEqual(name.withNS("bar")("foo"), "bar:foo")


class Test_stripNS (unittest.TestCase):

    def test_stripNS_preservesStringWithNoNamespaces (self):
        self.assertEqual(name.stripNS("nsfree"), "nsfree")

    def test_stripNS_removesOneNamespace (self):
        self.assertEqual(name.stripNS("foo:tball"), "tball")

    def test_stripNS_removesTwoNamespaces (self):
        self.assertEqual(name.stripNS("bar:foo:tball"), "tball")

    def test_stripNS_removesManyNamespaces (self):
        self.assertEqual(name.stripNS("a:b:c:d:e"), "e")


# @attr('maya')
@unittest.skipUnless(hasMaya, "requires Maya")
class Test_renameBy (unittest.TestCase):

    def setUp (self):
        self.loc = cmds.spaceLocator()[0]

    def test_renameBy_identity (self):
        result = name.renameBy(lambda x: x)(self.loc)
        self.assertTrue(cmds.objExists(self.loc))

    def test_renameBy_tail (self):
        result = name.renameBy(lambda x: x[1:])(self.loc)
        self.assertTrue(cmds.objExists(self.loc[1:]))

    def test_renameBy_doubling (self):
        result = name.renameBy(lambda x: x + x)(self.loc)
        self.assertTrue(cmds.objExists(self.loc + self.loc))

# @attr('maya')
@unittest.skipUnless(hasMaya, "requires Maya")
class Test_renameTo (unittest.TestCase):

    def setUp (self):
        self.loc = cmds.spaceLocator()[0]

    def test_renameTo_sameName (self):
        result = name.renameTo(self.loc)(self.loc)
        self.assertEqual(result, self.loc)

    def test_renameTo_simpleRename (self):
        result = name.renameTo("bob")(self.loc)
        self.assertEqual(result, "bob")

