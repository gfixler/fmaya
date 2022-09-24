import unittest
from nose.plugins.attrib import attr

import pure


class Test_ident (unittest.TestCase):

    def test_ident_preservesNumber (self):
        self.assertEqual(pure.ident(3), 3)

    def test_ident_preservesString (self):
        self.assertEqual(pure.ident("foo"), "foo")

    def test_ident_preservesEmptyList (self):
        self.assertEqual(pure.ident([]), [])

    def test_ident_preservesNone (self):
        self.assertEqual(pure.ident(None), None)


class Test_const (unittest.TestCase):

    def test_const_keepsStringOverNumber (self):
        self.assertEqual(pure.const("foo")(3), "foo")

    def test_const_keepsNoneOverBoolean (self):
        self.assertEqual(pure.const(None)(True), None)


class Test_app (unittest.TestCase):

    def test_app_respectsIdentity (self):
        self.assertEqual(pure.app(lambda x: x)("foo"), "foo")

    def test_app_appliesAFunction (self):
        self.assertEqual(pure.app(len)("hooberbloob"), 11)


class Test_flip (unittest.TestCase):

    def test_flip_flipsArgs (self):
        enlist = lambda x: lambda y: [x, y]
        self.assertEqual(pure.flip(enlist)("x")("y"), ["y","x"])


class Test_juxt (unittest.TestCase):

    def test_juxt_noFunctionsYieldsEmptyList (self):
        self.assertEqual(pure.juxt()(3), [])

    def test_juxt_oneFunctionYieldsOneCorrectResult (self):
        self.assertEqual(pure.juxt(len)("banana"), [6])

    def test_juxt_handlesSeveralFunctions (self):
        rev = lambda xs: xs[::-1]
        cap = lambda s: s.upper()
        self.assertEqual(pure.juxt(rev, len, cap)("function"), ["noitcnuf", 8, "FUNCTION"])


class Test_both (unittest.TestCase):

    def test_both_doesBoth (self):
        self.assertEqual(pure.both(lambda x: x)(lambda y: y[::-1])("cat"), ("cat", "tac"))


class Test_comp (unittest.TestCase):

    def test_comp_oneFunctionWorksAsApply (self):
        self.assertEqual(pure.comp(lambda x: x * 23)(42), 23 * 42)

    def test_comp_composesTwoFunctions (self):
        self.assertEqual(pure.comp(lambda x: x[::-1], lambda y: y[2:])("testing"), "gnits")

    def test_comp_composeFiveFunctions (self):
        chop = lambda x: x[1:]
        self.assertEqual(pure.comp(chop, chop, chop, chop, chop)("0123456"), "56")


class Test_cmap (unittest.TestCase):

    def test_cmap_mapsOverStrings (self):
        self.assertEqual(pure.cmap(lambda x: x[1:])(["one","two","three"]), ["ne","wo","hree"])

    def test_cmap_mapsOverNumbers (self):
        self.assertEqual(pure.cmap(lambda x: x*x)([1,3,8,5]), [1,9,64,25])

    def test_cmap_mapsOverBooleans (self):
        self.assertEqual(pure.cmap(lambda x: not x)([True,False,False,True]), [False,True,True,False])


class Test_czip (unittest.TestCase):

    def test_czip_emptyListsYieldEmptyList (self):
        self.assertEqual(pure.czip([])([]), [])

    def test_czip_emptyFirstListYieldsEmptyList (self):
        self.assertEqual(pure.czip([])([1,2,4]), [])

    def test_czip_emptySecondListYieldsEmptyList (self):
        self.assertEqual(pure.czip([8,3,1])([]), [])

    def test_czip_canZip2ListsOfSameLength (self):
        self.assertEqual(pure.czip([1,2,3])([4,5,6]), [(1,4),(2,5),(3,6)])

    def test_czip_shorterFirstListTruncatesSecondList (self):
        self.assertEqual(pure.czip([1,2,3])([4,5,6,7,8]), [(1,4),(2,5),(3,6)])

    def test_czip_shorterSecondListTruncatesFirstList (self):
        self.assertEqual(pure.czip([1,2,3,4,5])([6,7,8]), [(1,6),(2,7),(3,8)])


class Test_zipWith (unittest.TestCase):

    def test_zipWith_additionOfSameLengthLists (self):
        add = lambda x: lambda y: x + y
        self.assertEqual(pure.zipWith(add)([3,2,6,1,2])([5,5,3,2,5]), [8,7,9,3,7])

    def test_zipWith_concatenationOfMismatchedLists (self):
        conc = lambda x: lambda y: x + y
        a = ["dino","mega","beetle"]
        b = ["cat","dog","bird","frog"]
        expected = ["dinocat","megadog","beetlebird"]
        self.assertEqual(pure.zipWith(conc)(a)(b), expected)

    def test_zipWith_tupleWithEmptyList (self):
        entuple = lambda x: lambda y: (x, y)
        self.assertEqual(pure.zipWith(entuple)([])([1,2,3]), [])


class Test_curry2 (unittest.TestCase):

    def test_curry2_curriesAddition (self):
        add = lambda x, y: x + y
        self.assertEqual(pure.curry2(add)(7)(9), 16)

    def test_curry2_curriesComparison (self):
        lessThan = lambda x, y: x < y
        self.assertEqual(pure.curry2(lessThan)(7)(9), True)


class Test_uncurry2 (unittest.TestCase):

    def test_uncurry2_uncurriesAddition (self):
        add = lambda x: lambda y: x + y
        self.assertEqual(pure.uncurry2(add)(7, 9), 16)

    def test_uncurry2_uncurriesComparison (self):
        lessThan = lambda x: lambda y: x < y
        self.assertEqual(pure.uncurry2(lessThan)(7, 9), True)


class Test_uncurryPair (unittest.TestCase):

    def test_uncurryPair_uncurriesAddition (self):
        add = lambda x: lambda y: x + y
        self.assertEqual(pure.uncurryPair(add)((7, 9)), 16)

    def test_uncurryPair_uncurriesComparison (self):
        lessThan = lambda x: lambda y: x < y
        self.assertEqual(pure.uncurryPair(lessThan)((7, 9)), True)


class Test_fst (unittest.TestCase):

    def test_fst_getsFirstElementInTuple (self):
        self.assertEqual(pure.fst((3,"foo")), 3)

    def test_fst_getsFirstElementInAnotherTuple (self):
        self.assertEqual(pure.fst((False, "bar")), False)


class Test_snd (unittest.TestCase):

    def test_snd_getsSecondElementInTuple (self):
        self.assertEqual(pure.snd((3,"foo")), "foo")

    def test_snd_getsSecondElementInAnotherTuple (self):
        self.assertEqual(pure.snd((False, "bar")), "bar")


class Test_onFst (unittest.TestCase):

    def test_onFst_identityDoesNotChangeAnything (self):
        self.assertEqual(pure.onFst(lambda x: x)((3,"foo")), (3,"foo"))

    def test_onFst_worksOnFirstValue (self):
        self.assertEqual(pure.onFst(lambda x: x*2)((3,"foo")), (6,"foo"))


class Test_onSnd (unittest.TestCase):

    def test_onSnd_identityDoesNotChangeAnything (self):
        self.assertEqual(pure.onSnd(lambda x: x)((3,"foo")), (3,"foo"))

    def test_onSnd_worksOnSecondValue (self):
        self.assertEqual(pure.onSnd(lambda x: x[::-1])((3,"foo")), (3,"oof"))


class Test_swap (unittest.TestCase):

    def test_swap_swaps (self):
        self.assertEqual(pure.swap(('a',2)), (2,'a'))


class Test_concat (unittest.TestCase):

    def test_concatsStrings (self):
        self.assertEqual(pure.concat(["foo","bar","baz"]), "foobarbaz")

    def test_concatsNumberList (self):
        self.assertEqual(pure.concat([[1,2,3],[],[4,5],[6],[]]), [1,2,3,4,5,6])

    def test_concatsBooleanList (self):
        self.assertEqual(pure.concat([[True],[],[False,True],[False],[]]), [True,False,True,False])


class Test_isEmpty (unittest.TestCase):

    def test_isEmpty_emptyListIsEmpty (self):
        self.assertEqual(pure.isEmpty([]), True)

    def test_isEmpty_singleNumberListIsNotEmpty (self):
        self.assertEqual(pure.isEmpty([3]), False)

    def test_isEmpty_singletonStringListIsNotEmpty (self):
        self.assertEqual(pure.isEmpty(["foo"]), False)

    def test_isEmpty_multiElementBoolListIsNotEmpty (self):
        self.assertEqual(pure.isEmpty([True,False,False,True]), False)

    def test_isEmpty_stringIsNotEmpty (self):
        self.assertEqual(pure.isEmpty("foo"), False)

    def test_isEmpty_emptyStringIsEmpty (self):
        self.assertEqual(pure.isEmpty(""), True)


class Test_reverse (unittest.TestCase):

    def test_reverse_identityOnEmptyList (self):
        self.assertEqual(pure.reverse([]), [])

    def test_reverse_identityOnSingletonList (self):
        self.assertEqual(pure.reverse([1]), [1])

    def test_reverse_reverses2ElementList (self):
        self.assertEqual(pure.reverse([1,2]), [2,1])

    def test_reverse_reversesList (self):
        self.assertEqual(pure.reverse([4,3,2,6,1,4]), [4,1,6,2,3,4])

    def test_reverse_identityOnEmptyString (self):
        self.assertEqual(pure.reverse(""), "")

    def test_reverse_identityOnSingletonString (self):
        self.assertEqual(pure.reverse("c"), "c")

    def test_reverse_reverses2ElementString (self):
        self.assertEqual(pure.reverse("ab"), "ba")

    def test_reverse_reversesString (self):
        self.assertEqual(pure.reverse("testing"), "gnitset")


class Test__not (unittest.TestCase):

    def test__not_flipsTrueToFalse (self):
        self.assertEqual(pure._not(True), False)

    def test__not_flipsFalseToTrue (self):
        self.assertEqual(pure._not(False), True)


class Test_eq (unittest.TestCase):

    def test_eq_findsBooleanEquality (self):
        self.assertEqual(pure.eq(False)(False), True)

    def test_eq_findsBooleanInequality (self):
        self.assertEqual(pure.eq(True)(False), False)

    def test_eq_findsAlternateBooleanInequality (self):
        self.assertEqual(pure.eq(False)(True), False)

    def test_eq_findsNumericEquality (self):
        self.assertEqual(pure.eq(3)(3), True)

    def test_eq_findsNumericInequality (self):
        self.assertEqual(pure.eq(8)(3), False)

    def test_eq_findsStringEquality (self):
        self.assertEqual(pure.eq("foo")("foo"), True)

    def test_eq_findsStringInequality (self):
        self.assertEqual(pure.eq("bar")("foo"), False)


class Test_neq (unittest.TestCase):

    def test_neq_findsBooleanEquality (self):
        self.assertEqual(pure.neq(False)(False), False)

    def test_neq_findsBooleanInnequality (self):
        self.assertEqual(pure.neq(True)(False), True)

    def test_neq_findsAlternateBooleanInnequality (self):
        self.assertEqual(pure.neq(False)(True), True)

    def test_neq_findsNumericEquality (self):
        self.assertEqual(pure.neq(3)(3), False)

    def test_neq_findsNumericInnequality (self):
        self.assertEqual(pure.neq(8)(3), True)

    def test_neq_findsStringEquality (self):
        self.assertEqual(pure.neq("foo")("foo"), False)

    def test_neq_findsStringInnequality (self):
        self.assertEqual(pure.neq("bar")("foo"), True)


class Test_begins (unittest.TestCase):

    def test_begins_begins (self):
        self.assertEqual(pure.begins("foo")("foobar"), True)

    def test_begins_doesNotBegin (self):
        self.assertEqual(pure.begins("foo")("barquux"), False)

    def test_begins_fullMatchCounts (self):
        self.assertEqual(pure.begins("foo")("foo"), True)

    def test_begins_emptyPrefixAlwaysMatches (self):
        self.assertEqual(pure.begins("")("nonempty"), True)

    def test_begins_anyMatchOnEmptyIsFalse (self):
        self.assertEqual(pure.begins("test")(""), False)

    def test_begins_twoEmptyStringsMatch (self):
        self.assertEqual(pure.begins("")(""), True)


class Test_ends (unittest.TestCase):

    def test_ends_ends (self):
        self.assertEqual(pure.ends("bar")("foobar"), True)

    def test_ends_doesNotEnd (self):
        self.assertEqual(pure.ends("foo")("barquux"), False)

    def test_ends_emptyPrefixAlwaysMatches (self):
        self.assertEqual(pure.ends("")("nonempty"), True)

    def test_ends_fullMatchCounts (self):
        self.assertEqual(pure.ends("foo")("foo"), True)

    def test_ends_anyMatchOnEmptyIsFalse (self):
        self.assertEqual(pure.ends("test")(""), False)

    def test_ends_twoEmptyStringsMatch (self):
        self.assertEqual(pure.ends("")(""), True)


class Test_preadd (unittest.TestCase):

    def test_preadd_canAddNumbers (self):
        self.assertEqual(pure.preadd(3)(4), 7)

    def test_preadd_canPrependToString (self):
        self.assertEqual(pure.preadd("foo")("bar"), "foobar")

    def test_preadd_canPrependNumberList (self):
        self.assertEqual(pure.preadd([1,2,3])([4,5]), [1,2,3,4,5])


class Test_postadd (unittest.TestCase):

    def test_postadd_canAddNumbers (self):
        self.assertEqual(pure.postadd(3)(4), 7)

    def test_postadd_canPostpendString (self):
        self.assertEqual(pure.postadd("foo")("bar"), "barfoo")

    def test_postadd_canPrependNumberList (self):
        self.assertEqual(pure.postadd([1,2,3])([4,5]), [4,5,1,2,3])


class Test_unprefix (unittest.TestCase):

    def test_unprefix_nullPrefixIsIdentity (self):
        self.assertEqual(pure.unprefix("")("testing"), "testing")

    def test_unprefix_prefixNotFoundIsIdentity (self):
        self.assertEqual(pure.unprefix("nope")("whatever"), "whatever")

    def test_unprefix_removesPrefix (self):
        self.assertEqual(pure.unprefix("cat")("catdog"), "dog")

    def test_unprefix_handlesEmptyInput (self):
        self.assertEqual(pure.unprefix("uhoh")(""), "")

    def test_unprefix_handlesBothEmptyStrings (self):
        self.assertEqual(pure.unprefix("")(""), "")


class Test_unsuffix (unittest.TestCase):

    def test_unsuffix_nullPrefixIsIdentity (self):
        self.assertEqual(pure.unsuffix("")("testing"), "testing")

    def test_unsuffix_suffixNotFoundIsIdentity (self):
        self.assertEqual(pure.unsuffix("nope")("whatever"), "whatever")

    def test_unsuffix_removesPrefix (self):
        self.assertEqual(pure.unsuffix("dog")("catdog"), "cat")

    def test_unsuffix_handlesEmptyInput (self):
        self.assertEqual(pure.unsuffix("uhoh")(""), "")

    def test_unsuffix_handlesBothEmptyStrings (self):
        self.assertEqual(pure.unsuffix("")(""), "")


class Test_mid (unittest.TestCase):

    def test_mid_findsSameNumberGivenTwice (self):
        self.assertEqual(pure.mid(7)(7), 7)

    def test_mid_findsMidpoint (self):
        self.assertEqual(pure.mid(3)(7), 5)

    def test_mid_findsMidpointWithNegative (self):
        self.assertEqual(pure.mid(-9)(7), -1)


class Test_filterBy (unittest.TestCase):

    def test_filterBy_keepTrueValues (self):
        self.assertEqual(pure.filterBy(lambda b: b)([False,True,True,False,True]), [True,True,True])

    def test_filterBy_keepFalseValues (self):
        self.assertEqual(pure.filterBy(lambda b: not b)([False,True,True,False,True]), [False,False])

    def test_filterBy_keepValuesGreaterThan5 (self):
        self.assertEqual(pure.filterBy(lambda n: n > 5)([2,3,6,4,7,2,1,7,4,6,8,4]), [6,7,7,6,8])

    def test_filterBy_specialCasesStringsToAvoidConversionToList (self):
        self.assertEqual(pure.filterBy(lambda c: c in "aeiou")("eleanor"), "eeao")


class Test_firstBy (unittest.TestCase):

    def test_firstBy_findsValueInFirstPosition (self):
        self.assertEqual(pure.firstBy(lambda x: x == 3)([3,4,5,2,1]), 3)

    def test_firstBy_findsValueInLastPosition (self):
        self.assertEqual(pure.firstBy(lambda x: x == 1)([3,4,5,2,1]), 1)

    def test_firstBy_findsValueInMiddle (self):
        self.assertEqual(pure.firstBy(lambda x: x == 5)([3,4,5,2,1]), 5)

    def test_firstBy_findsBySecondElementInTuple (self):
        self.assertEqual(pure.firstBy(lambda xy: xy[1] == 3)([(0,1),(2,3),(4,5),(6,7)]), (2,3))

    def test_firstBy_raisesOnUnfoundElement (self):
        self.assertRaises(IndexError, lambda: pure.firstBy(lambda _: False)([1,2,3,4,5]))

    def test_firstBy_raisesOnEmptyList (self):
        self.assertRaises(IndexError, lambda: pure.firstBy(lambda _: True)([]))


class Test_anyBy (unittest.TestCase):

    def test_anyBy_constTrueYieldsTrue (self):
        self.assertEqual(pure.anyBy(lambda _: True)([1,3,7,8,9]), True)

    def test_anyBy_constFalseYieldsFalse (self):
        self.assertEqual(pure.anyBy(lambda _: False)([1,3,7,8,9]), False)

    def test_anyBy_returnsTrueOnMatchingALetter (self):
        self.assertEqual(pure.anyBy(lambda x: x == 'e')("awesome"), True)

    def test_anyBy_returnsFalseWhenNoNumberIsGreatEnough (self):
        self.assertEqual(pure.anyBy(lambda x: x > 5)([1,2,4,2,1,3,2,4,1]), False)

    def test_anyBy_returnsTrueWhenANumberIsGreatEnough (self):
        self.assertEqual(pure.anyBy(lambda x: x > 5)([1,2,4,2,7,3,2,4,1]), True)


class Test_minBy (unittest.TestCase):

    def test_minBy_identity (self):
        self.assertEqual(pure.minBy(lambda x: x)([5,3,6,2,3,4]), 2)

    def test_minBy_length (self):
        # also gives evidence that it's a stable sort
        self.assertEqual(pure.minBy(len)(["three","seven","six","four","two"]), "six")


class Test_maxBy (unittest.TestCase):

    def test_maxBy_identity (self):
        self.assertEqual(pure.maxBy(lambda x: x)([5,3,6,2,3,4]), 6)

    def test_maxBy_length (self):
        # also gives evidence that it's a stable sort
        self.assertEqual(pure.maxBy(len)(["three","seven","six","four","two"]), "seven")


class Test_minAndMax (unittest.TestCase):

    def test_minAndMax_raisesOnEmptyList (self):
        self.assertRaises(ValueError, lambda: pure.minAndMax([]))

    def test_minAndMax_findsOnlyElementInSingletonList (self):
        self.assertEqual(pure.minAndMax([3]), (3, 3))

    def test_minAndMax_findsMinAndMaxInLengthNList (self):
        self.assertEqual(pure.minAndMax([3,4,2,8,1,2,7]), (1, 8))


class Test_iterateTimes (unittest.TestCase):

    def test_iterateTimes_identity (self):
        self.assertEqual(pure.iterateTimes(5)(lambda x: x)("foo"), "foo")

    def test_iterateTimes_incrementation (self):
        self.assertEqual(pure.iterateTimes(7)(lambda x: x + 1)(5), 12)

    def test_iterateTimes_doubling (self):
        self.assertEqual(pure.iterateTimes(16)(lambda x: x * 2)(1), 65536)

    def test_iterateTimes_concatenation (self):
        self.assertEqual(pure.iterateTimes(5)(lambda x: x + "cat")(""), "catcatcatcatcat")


class Test_lerp (unittest.TestCase):

    def test_lerp_0YieldsFirstPoint (self):
        self.assertEqual(pure.lerp(0)(3)(7), 3)

    def test_lerp_1YieldsSecondPoint (self):
        self.assertEqual(pure.lerp(1)(3)(7), 7)

    def test_lerp_0_5YieldsMidpoint (self):
        self.assertEqual(pure.lerp(0.5)(3)(7), 5.0)


class Test_grep (unittest.TestCase):

    def test_grep_emptyStringPatternReturnsEntireList (self):
        stream = ["foo","bar","baz"]
        self.assertEqual(pure.grep('')(stream), stream)

    def test_grep_findsLiterals (self):
        given = ["apple","banana","banana_apple","apple-pen","grapple","appple"]
        expected = ["apple","banana_apple","apple-pen","grapple"]
        self.assertEqual(pure.grep('apple')(given), expected)

    def test_grep_findsAtBeginning (self):
        self.assertEqual(pure.grep("^abc")(["abc","cabc","abcdef"]), ["abc","abcdef"])

    def test_grep_findsAtEnd (self):
        given = ["!","!?","yay!","ah!ha","woo!!!"]
        expected = ["!","yay!","woo!!!"]
        self.assertEqual(pure.grep("!$")(given), expected)

    def test_grep_findsARealisticRegex (self):
        given = ["a:b","a:b:c","a","b","a:b:d","a:e","::"]
        expected = ["a:b:c","a:b:d","::"]
        self.assertEqual(pure.grep("^[^:]*:[^:]*:[^:]*$")(given), expected)

