import unittest
from nose.plugins.attrib import attr

from .. import pure


class Test_ident (unittest.TestCase):

    def test_ident_preservesNumber (self):
        self.assertEquals(pure.ident(3), 3)

    def test_ident_preservesString (self):
        self.assertEquals(pure.ident("foo"), "foo")

    def test_ident_preservesEmptyList (self):
        self.assertEquals(pure.ident([]), [])

    def test_ident_preservesNone (self):
        self.assertEquals(pure.ident(None), None)


class Test_const (unittest.TestCase):

    def test_const_keepsStringOverNumber (self):
        self.assertEquals(pure.const("foo")(3), "foo")

    def test_const_keepsNoneOverBoolean (self):
        self.assertEquals(pure.const(None)(True), None)


class Test_comp (unittest.TestCase):

    def test_comp_oneFunctionWorksAsApply (self):
        self.assertEquals(pure.comp(lambda x: x * 23)(42), 23 * 42)

    def test_comp_composesTwoFunctions (self):
        self.assertEquals(pure.comp(lambda x: x[::-1], lambda y: y[2:])("testing"), "gnits")

    def test_comp_composeFiveFunctions (self):
        chop = lambda x: x[1:]
        self.assertEquals(pure.comp(chop, chop, chop, chop, chop)("0123456"), "56")


class Test_cmap (unittest.TestCase):

    def test_cmap_mapsOverStrings (self):
        self.assertEquals(pure.cmap(lambda x: x[1:])(["one","two","three"]), ["ne","wo","hree"])

    def test_cmap_mapsOverNumbers (self):
        self.assertEquals(pure.cmap(lambda x: x*x)([1,3,8,5]), [1,9,64,25])

    def test_cmap_mapsOverBooleans (self):
        self.assertEquals(pure.cmap(lambda x: not x)([True,False,False,True]), [False,True,True,False])


class Test_curry (unittest.TestCase):

    def test_curry_curriesAddition (self):
        add = lambda x, y: x + y
        self.assertEquals(pure.curry(add)(7)(9), 16)

    def test_curry_curriesComparison (self):
        lessThan = lambda x, y: x < y
        self.assertEquals(pure.curry(lessThan)(7)(9), True)


class Test_uncurry (unittest.TestCase):

    def test_uncurry_uncurriesAddition (self):
        add = lambda x: lambda y: x + y
        self.assertEquals(pure.uncurry(add)((7, 9)), 16)

    def test_uncurry_uncurriesComparison (self):
        lessThan = lambda x: lambda y: x < y
        self.assertEquals(pure.uncurry(lessThan)((7, 9)), True)

