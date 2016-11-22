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


class Test_fst (unittest.TestCase):

    def test_fst_getsFirstElementInTuple (self):
        self.assertEquals(pure.fst((3,"foo")), 3)

    def test_fst_getsFirstElementInAnotherTuple (self):
        self.assertEquals(pure.fst((False, "bar")), False)


class Test_snd (unittest.TestCase):

    def test_snd_getsSecondElementInTuple (self):
        self.assertEquals(pure.snd((3,"foo")), "foo")

    def test_snd_getsSecondElementInAnotherTuple (self):
        self.assertEquals(pure.snd((False, "bar")), "bar")


class Test_concat (unittest.TestCase):

    def test_concatsStrings (self):
        self.assertEquals(pure.concat(["foo","bar","baz"]), "foobarbaz")

    def test_concatsNumberList (self):
        self.assertEquals(pure.concat([[1,2,3],[],[4,5],[6],[]]), [1,2,3,4,5,6])

    def test_concatsBooleanList (self):
        self.assertEquals(pure.concat([[True],[],[False,True],[False],[]]), [True,False,True,False])


class Test_isEmpty (unittest.TestCase):

    def test_isEmpty_emptyListIsEmpty (self):
        self.assertEquals(pure.isEmpty([]), True)

    def test_isEmpty_singleNumberListIsNotEmpty (self):
        self.assertEquals(pure.isEmpty([3]), False)

    def test_isEmpty_singletonStringListIsNotEmpty (self):
        self.assertEquals(pure.isEmpty(["foo"]), False)

    def test_isEmpty_multiElementBoolListIsNotEmpty (self):
        self.assertEquals(pure.isEmpty([True,False,False,True]), False)

    def test_isEmpty_stringIsNotEmpty (self):
        self.assertEquals(pure.isEmpty("foo"), False)

    def test_isEmpty_emptyStringIsEmpty (self):
        self.assertEquals(pure.isEmpty(""), True)


class Test_bnot (unittest.TestCase):

    def test_bnot_flipsTrueToFalse (self):
        self.assertEquals(pure.bnot(True), False)

    def test_bnot_flipsFalseToTrue (self):
        self.assertEquals(pure.bnot(False), True)


class Test_eq (unittest.TestCase):

    def test_eq_findsBooleanEquality (self):
        self.assertEquals(pure.eq(False)(False), True)

    def test_eq_findsBooleanInequality (self):
        self.assertEquals(pure.eq(True)(False), False)

    def test_eq_findsAlternateBooleanInequality (self):
        self.assertEquals(pure.eq(False)(True), False)

    def test_eq_findsNumericEquality (self):
        self.assertEquals(pure.eq(3)(3), True)

    def test_eq_findsNumericInequality (self):
        self.assertEquals(pure.eq(8)(3), False)

    def test_eq_findsStringEquality (self):
        self.assertEquals(pure.eq("foo")("foo"), True)

    def test_eq_findsStringInequality (self):
        self.assertEquals(pure.eq("bar")("foo"), False)


class Test_neq (unittest.TestCase):

    def test_neq_findsBooleanEquality (self):
        self.assertEquals(pure.neq(False)(False), False)

    def test_neq_findsBooleanInnequality (self):
        self.assertEquals(pure.neq(True)(False), True)

    def test_neq_findsAlternateBooleanInnequality (self):
        self.assertEquals(pure.neq(False)(True), True)

    def test_neq_findsNumericEquality (self):
        self.assertEquals(pure.neq(3)(3), False)

    def test_neq_findsNumericInnequality (self):
        self.assertEquals(pure.neq(8)(3), True)

    def test_neq_findsStringEquality (self):
        self.assertEquals(pure.neq("foo")("foo"), False)

    def test_neq_findsStringInnequality (self):
        self.assertEquals(pure.neq("bar")("foo"), True)


class Test_preadd (unittest.TestCase):

    def test_preadd_canAddNumbers (self):
        self.assertEquals(pure.preadd(3)(4), 7)

    def test_preadd_canPrependToString (self):
        self.assertEquals(pure.preadd("foo")("bar"), "foobar")

    def test_preadd_canPrependNumberList (self):
        self.assertEquals(pure.preadd([1,2,3])([4,5]), [1,2,3,4,5])


class Test_postadd (unittest.TestCase):

    def test_postadd_canAddNumbers (self):
        self.assertEquals(pure.postadd(3)(4), 7)

    def test_postadd_canPostpendString (self):
        self.assertEquals(pure.postadd("foo")("bar"), "barfoo")

    def test_postadd_canPrependNumberList (self):
        self.assertEquals(pure.postadd([1,2,3])([4,5]), [4,5,1,2,3])


class Test_mid (unittest.TestCase):

    def test_mid_findsSameNumberGivenTwice (self):
        self.assertEquals(pure.mid(7)(7), 7)

    def test_mid_findsMidpoint (self):
        self.assertEquals(pure.mid(3)(7), 5)

    def test_mid_findsMidpointWithNegative (self):
        self.assertEquals(pure.mid(-9)(7), -1)


class Test_filt (unittest.TestCase):

    def test_filt_keepTrueValues (self):
        self.assertEquals(pure.filt(lambda b: b)([False,True,True,False,True]), [True,True,True])

    def test_filt_keepFalseValues (self):
        self.assertEquals(pure.filt(lambda b: not b)([False,True,True,False,True]), [False,False])

    def test_filt_keepValuesGreaterThan5 (self):
        self.assertEquals(pure.filt(lambda n: n > 5)([2,3,6,4,7,2,1,7,4,6,8,4]), [6,7,7,6,8])

    def test_filt_keepVowelsInString (self):
        self.assertEquals(pure.filt(lambda c: c in "aeiou")("eleanor"), "eeao")
