import unittest
from nose.plugins.attrib import attr

try:
    import maya.cmds as cmds
except ImportError:
    print 'WARNING (%s): failed to load maya.cmds module.' % __file__

import hier


@attr('maya')
class Test_getParent (unittest.TestCase):

    def setUp (self):
        cmds.file(new=True, force=True)

    def test_getParent_returnsNoneOnRootObject (self):
        self.assertEqual(hier.getParent("persp"), None)

    def test_getParent_returnsParentIfOneExists (self):
        a = cmds.spaceLocator()[0]
        b = cmds.spaceLocator()[0]
        a2 = cmds.parent(a, b)
        self.assertEqual(hier.getParent(a2), b)


@attr('maya')
class Test_withParent (unittest.TestCase):

    def setUp (self):
        cmds.file(new=True, force=True)

    def test_withParent_returnsDefaultWhenNoParent (self):
        self.assertEqual(hier.withParent("nope")(lambda x: x)("persp"), "nope")

    def test_withParent_returnsParentViaIdentityFunction (self):
        a = cmds.spaceLocator()[0]
        b = cmds.spaceLocator()[0]
        a2 = cmds.parent(a, b)
        self.assertEqual(hier.withParent("default")(lambda x: x)(a2), b)

    def test_withParent_canRunPredicatesOnTheParent (self):
        a = cmds.spaceLocator()[0]
        b = cmds.spaceLocator(name="dad")[0]
        a2 = cmds.parent(a, b)
        self.assertTrue(hier.withParent(False)(lambda x: x == "dad")(a2))
        self.assertFalse(hier.withParent(False)(lambda x: x == "mom")(a2))


@attr('maya')
class Test_parentPred (unittest.TestCase):

    def setUp (self):
        cmds.file(new=True, force=True)

    def test_parentPred_canCheckForExistence (self):
        a = cmds.spaceLocator()[0]
        b = cmds.spaceLocator()[0]
        a2 = cmds.parent(a, b)[0]
        self.assertTrue(hier.parentPred(lambda x: x)(a2))

    def test_parentPred_canCheckName (self):
        a = cmds.spaceLocator()[0]
        b = cmds.spaceLocator()[0]
        a2 = cmds.parent(a, b)[0]
        self.assertTrue(hier.parentPred(lambda x: x == b)(a2))


@attr('maya')
class Test_parentNameIs (unittest.TestCase):

    def setUp (self):
        cmds.file(new=True, force=True)

    def test_parentNameIs_returnsFalseWhenNoParent (self):
        self.assertFalse(hier.parentNameIs("foo")("persp"))

    def test_parentNameIs_returnsFalseWhenNameDoesNotMatch (self):
        a = cmds.spaceLocator()[0]
        b = cmds.spaceLocator()[0]
        a2 = cmds.parent(a, b)[0]
        self.assertFalse(hier.parentNameIs("wrongname")(a2))

    def test_parentNameIs_returnsTrueWhenNameMatches (self):
        a = cmds.spaceLocator()[0]
        b = cmds.spaceLocator()[0]
        a2 = cmds.parent(a, b)[0]
        self.assertTrue(hier.parentNameIs(b)(a2))

