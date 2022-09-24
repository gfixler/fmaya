import unittest
from nose.plugins.attrib import attr
from functools import reduce

from math import sqrt

try:
    import maya.cmds as cmds
    hasMaya = True
except ImportError:
    print('WARNING (%s): failed to load maya.cmds module.' % __file__)
    hasMaya = False

import tf


# PURE

class Test_xyzAdd (unittest.TestCase):

    def test_xyzAdd_identities (self):
        self.assertEqual(tf.xyzAdd((0,0,0))((0,0,0)), (0,0,0))

    def test_xyzAdd_leftIdentity (self):
        self.assertEqual(tf.xyzAdd((0,0,0))((2,1,5)), (2,1,5))

    def test_xyzAdd_rightIdentity (self):
        self.assertEqual(tf.xyzAdd((3,2,5))((0,0,0)), (3,2,5))

    def test_xyzAdd_positives (self):
        self.assertEqual(tf.xyzAdd((3,2,5))((2,1,1)), (5,3,6))

    def test_xyzAdd_negatives (self):
        self.assertEqual(tf.xyzAdd((-2,-3,-1))((-2,-1,-3)), (-4,-4,-4))

    def test_xyzAdd_negativesAndPositives (self):
        self.assertEqual(tf.xyzAdd((-2,3,1))((2,-1,3)), (0,2,4))


class Test_xyzSub (unittest.TestCase):

    def test_xyzSub_identities (self):
        self.assertEqual(tf.xyzSub((0,0,0))((0,0,0)), (0,0,0))

    def test_xyzSub_noLeftIdentity (self):
        self.assertEqual(tf.xyzSub((0,0,0))((2,1,5)), (-2,-1,-5))

    def test_xyzSub_rightIdentity (self):
        self.assertEqual(tf.xyzSub((3,2,5))((0,0,0)), (3,2,5))

    def test_xyzSub_positives (self):
        self.assertEqual(tf.xyzSub((3,2,5))((2,1,1)), (1,1,4))

    def test_xyzSub_negatives (self):
        self.assertEqual(tf.xyzSub((-2,-3,-1))((-2,-1,-3)), (0,-2,2))

    def test_xyzSub_negativesAndPositives (self):
        self.assertEqual(tf.xyzSub((-2,3,1))((2,-1,3)), (-4,4,-2))


class Test_xyzMul (unittest.TestCase):

    def test_xyzMul_zeroes (self):
        self.assertEqual(tf.xyzMul((0,0,0))((0,0,0)), (0,0,0))

    def test_xyzMul_identities (self):
        self.assertEqual(tf.xyzMul((1,1,1))((1,1,1)), (1,1,1))

    def test_xyzMul_leftIdentity (self):
        self.assertEqual(tf.xyzMul((1,1,1))((2,1,5)), (2,1,5))

    def test_xyzMul_rightIdentity (self):
        self.assertEqual(tf.xyzMul((3,2,5))((1,1,1)), (3,2,5))

    def test_xyzMul_positives (self):
        self.assertEqual(tf.xyzMul((3,2,5))((2,1,1)), (6,2,5))

    def test_xyzMul_negatives (self):
        self.assertEqual(tf.xyzMul((-2,-3,-1))((-2,-1,-3)), (4,3,3))

    def test_xyzMul_negativesAndPositives (self):
        self.assertEqual(tf.xyzMul((-2,3,1))((2,-1,3)), (-4,-3,3))


class Test_xyzDiv (unittest.TestCase):

    def test_xyzDiv_dividingByZeroesRaises (self):
        self.assertRaises(ZeroDivisionError, lambda: tf.xyzDiv((1,1,1))((0,0,0)))

    def test_xyzDiv_identities (self):
        self.assertEqual(tf.xyzDiv((1,1,1))((1,1,1)), (1.0,1.0,1.0))

    def test_xyzDiv_noLeftIdentity (self):
        self.assertEqual(tf.xyzDiv((1,1,1))((2,1,5)), (0.5,1.0,0.2))

    def test_xyzDiv_rightIdentity (self):
        self.assertEqual(tf.xyzDiv((3,2,5))((1,1,1)), (3.0,2.0,5.0))

    def test_xyzDiv_allResultsPreservedAsOrPromotedToFloats (self):
        x, y, z = tf.xyzDiv((9,7,13))((3,3,4))
        self.assertTrue(type(x) == float and type(y) == float and type(z) == float)

    def test_xyzDiv_positives (self):
        self.assertEqual(tf.xyzDiv((3,2,5))((2,1,1)), (1.5,2.0,5.0))

    def test_xyzDiv_negatives (self):
        self.assertEqual(tf.xyzDiv((-2,-3,-3))((-2,-1,-3)), (1.0,3.0,1.0))

    def test_xyzDiv_negativesAndPositives (self):
        self.assertEqual(tf.xyzDiv((-2,3,3))((2,-1,3)), (-1.0,-3.0,1.0))


class Test_xyzScale (unittest.TestCase):

    def test_xyzScale_zeroZeroOut (self):
        self.assertEqual(tf.xyzScale(0)((-2,3,3)), (0,0,0))

    def test_xyzScale_hasIdentity (self):
        self.assertEqual(tf.xyzScale(1)((-2,3,1)), (-2,3,1))

    def test_xyzScale_scales (self):
        self.assertEqual(tf.xyzScale(3)((-2,3,1)), (-6,9,3))

    def test_xyzScale_inverseScales (self):
        self.assertEqual(tf.xyzScale(-1)((-2,3,1)), (2,-3,-1))


class Test_xyzSum (unittest.TestCase):

    def test_xyzSum_preservesIdentity (self):
        self.assertEqual(tf.xyzSum([]), (0,0,0))

    def test_xyzSum_keepsSingletonElement (self):
        self.assertEqual(tf.xyzSum([(2,-1,3)]), (2,-1,3))

    def test_xyzSum_sumsElements (self):
        self.assertEqual(tf.xyzSum([(2,-1,3),(1,1,2),(-3,2,-2),(-3,-1,2)]), (-3,1,5))


class Test_xyzAvg (unittest.TestCase):

    def test_xyzAvg_preservesIdentity (self):
        self.assertEqual(tf.xyzAvg([]), (0,0,0))

    def test_xyzAvg_keepsSingletonElement (self):
        self.assertEqual(tf.xyzAvg([(2,1,-3)]), (2,1,-3))

    def test_xyzAvg_sameTriplesAverageToThemselves (self):
        (x,y,z) = tf.xyzAvg([(1,2,3)] * 35)
        self.assertAlmostEqual(x, 1)
        self.assertAlmostEqual(y, 2)
        self.assertAlmostEqual(z, 3)

    def test_xyzAvg_averagesSomeIntegers (self):
        self.assertEqual(tf.xyzAvg([(1,2,3),(2,3,1),(3,4,-3),(2,3,-1)]), (2,3,0))


class Test_xyzDist (unittest.TestCase):

    def test_xyzDist_zeroWhenBothPointsAtOrigin (self):
        self.assertEqual(tf.xyzDist((0,0,0))((0,0,0)), 0.0)

    def test_xyzDist_zeroWhenBothPointsMatchAllPositive (self):
        self.assertEqual(tf.xyzDist((1,3,2))((1,3,2)), 0.0)

    def test_xyzDist_zeroWhenBothPointsMatchAllPositive (self):
        self.assertEqual(tf.xyzDist((-2,-4,-1))((-2,-4,-1)), 0.0)

    def test_xyzDist_getsLengthDownXAxisOnly (self):
        self.assertEqual(tf.xyzDist((1,2,3))((6,2,3)), 5.0)

    def test_xyzDist_getsLengthDownYAxisOnly (self):
        self.assertEqual(tf.xyzDist((1,2,3))((1,12,3)), 10.0)

    def test_xyzDist_getsLengthDownZAxisOnly (self):
        self.assertEqual(tf.xyzDist((1,2,3))((1,2,18)), 15.0)

    def test_xyzDist_345TriangleInXYPlane (self):
        self.assertEqual(tf.xyzDist((0,0,0))((3,4,0)), 5.0)

    def test_xyzDist_345TriangleInYZPlane (self):
        self.assertEqual(tf.xyzDist((0,0,0))((0,4,3)), 5.0)


class Test_xyzHypot (unittest.TestCase):

    def test_xyzHypot_zeroAtOrigin (self):
        self.assertEqual(tf.xyzHypot((0,0,0)), 0.0)

    def test_xyzHypot_345TriangleInXYPlane (self):
        self.assertEqual(tf.xyzHypot((3,4,0)), 5.0)

    def test_xyzHypot_345TriangleInXZPlane (self):
        self.assertEqual(tf.xyzHypot((3,0,4)), 5.0)

    def test_xyzHypot_345TriangleInYZPlane (self):
        self.assertEqual(tf.xyzHypot((0,3,4)), 5.0)

    def test_xyzHypot_unitCubeDiagonalEqualsSquareRootOf3 (self):
        self.assertEqual(tf.xyzHypot((1,1,1)), sqrt(3))


class Test_xyzUnit (unittest.TestCase):

    def test_xyzUnit_preservesXIdentity (self):
        self.assertEqual(tf.xyzUnit((1,0,0)), (1,0,0))

    def test_xyzUnit_preservesYIdentity (self):
        self.assertEqual(tf.xyzUnit((0,1,0)), (0,1,0))

    def test_xyzUnit_preservesZIdentity (self):
        self.assertEqual(tf.xyzUnit((0,0,1)), (0,0,1))

    def test_xyzUnit_shrinksAlongX (self):
        self.assertEqual(tf.xyzUnit((5,0,0)), (1,0,0))

    def test_xyzUnit_expandsAlongX (self):
        self.assertEqual(tf.xyzUnit((0.1,0,0)), (1,0,0))

    def test_xyzUnit_shrinksAlongY (self):
        self.assertEqual(tf.xyzUnit((0,5,0)), (0,1,0))

    def test_xyzUnit_expandsAlongY (self):
        self.assertEqual(tf.xyzUnit((0,0.1,0)), (0,1,0))

    def test_xyzUnit_shrinksAlongZ (self):
        self.assertEqual(tf.xyzUnit((0,0,5)), (0,0,1))

    def test_xyzUnit_expandsAlongZ (self):
        self.assertEqual(tf.xyzUnit((0,0,0.1)), (0,0,1))

    def test_xyzUnit_hypotOfResultIs1 (self):
        self.assertEqual(tf.xyzHypot(tf.xyzUnit((23.3,-12.8,4.2))), 1.0)


class Test_V3 (unittest.TestCase):

    def test_V3_canInstantitateAndReadDefaultXYZValues (self):
        v3 = tf.V3()
        self.assertEqual(v3.xyz, (0,0,0))

    def test_V3_canInstantiateWithXYZValues (self):
        v3 = tf.V3((3,7,4))
        self.assertEqual(v3.xyz, (3,7,4))

    def test_V3_convertsToTupleUnderTheHood (self):
        v3 = tf.V3([1,2,3])
        self.assertEqual(v3.xyz, (1,2,3))

    def test_V3_canGetXValue (self):
        v3 = tf.V3((2,3,4))
        self.assertEqual(v3.x, 2)

    def test_V3_canSetXValue (self):
        v3 = tf.V3((5,6,7))
        v3.x = 9
        self.assertEqual(v3.xyz, (9,6,7))

    def test_V3_canGetYValue (self):
        v3 = tf.V3((2,3,4))
        self.assertEqual(v3.y, 3)

    def test_V3_canSetXValue (self):
        v3 = tf.V3((5,6,7))
        v3.y = 11
        self.assertEqual(v3.xyz, (5,11,7))

    def test_V3_canGetZValue (self):
        v3 = tf.V3((2,3,4))
        self.assertEqual(v3.z, 4)

    def test_V3_canSetXValue (self):
        v3 = tf.V3((5,6,7))
        v3.z = 13
        self.assertEqual(v3.xyz, (5,6,13))

    def test_V3_reprIncluesV3Tag (self):
        v3 = tf.V3((2,4,8))
        self.assertEqual(repr(v3), "V3 (2, 4, 8)")

    def test_V3_equality (self):
        self.assertEqual(tf.V3((1,2,3)), tf.V3((1,2,3)))

    def test_V3_inequality (self):
        self.assertNotEqual(tf.V3((2,2,3)), tf.V3((1,2,3)))

    def test_V3_canAddV3s (self):
        self.assertEqual(tf.V3((-2,3,1)) + tf.V3((1,2,3)), tf.V3((-1,5,4)))

    def test_V3_additionHasLeftIdentity (self):
        self.assertEqual(tf.V3((0,0,0)) + tf.V3((-2,3,1)), tf.V3((-2,3,1)))

    def test_V3_additionHasRightIdentity (self):
        self.assertEqual(tf.V3((-2,3,1)) + tf.V3((0,0,0)), tf.V3((-2,3,1)))

    def test_V3_canAddIntOnRight (self):
        self.assertEqual(tf.V3((3,1,2)) + 5, tf.V3((8,6,7)))

    def test_V3_canAddIntOnLeft (self):
        self.assertEqual(3 + tf.V3((3,1,2)), tf.V3((6,4,5)))

    def test_V3_canSumV3s (self):
        self.assertEqual(sum([tf.V3((1,2,3)),tf.V3((3,2,2)),tf.V3((3,2,2))]), tf.V3((7,6,7)))

    def test_V3_canReduceV3sWithAddition (self):
        v3s = [tf.V3((1,2,3)), tf.V3((2,1,1)), tf.V3((-2,-3,1)), tf.V3((-2,2,3))]
        result = reduce(lambda x, y: x + y, v3s)
        self.assertEqual(result, tf.V3((-1,2,8)))

    def test_V3_canSubtractV3s (self):
        self.assertEqual(tf.V3((2,4,1)) - tf.V3((-1,3,2)), tf.V3((3,1,-1)))

    def test_V3_subtractionHasRightIdentity (self):
        self.assertEqual(tf.V3((3,1,2)) - tf.V3((0,0,0)), tf.V3((3,1,2)))

    def test_V3_canMultiplyV3s (self):
        self.assertEqual(tf.V3((1,2,3)) * tf.V3((2,3,1)), tf.V3((2,6,3)))

    def test_V3_multiplicationHasLeftIdentity (self):
        self.assertEqual(tf.V3((1,1,1)) * tf.V3((-2,3,1)), tf.V3((-2,3,1)))

    def test_V3_multiplicationHasRightIdentity (self):
        self.assertEqual(tf.V3((-2,3,1)) * tf.V3((1,1,1)), tf.V3((-2,3,1)))

    def test_V3_canReduceV3sWithMultiplication (self):
        v3s = [tf.V3((1,2,3)), tf.V3((2,1,1)), tf.V3((-2,-3,1)), tf.V3((-2,2,3))]
        result = reduce(lambda x, y: x * y, v3s)
        self.assertEqual(result, tf.V3((8,-12,9)))

    def test_V3_canScaleByMultiplyingWithAnIntOnTheLeft (self):
        self.assertEqual(tf.V3((1,3,2)) * 3, tf.V3((3,9,6)))

    def test_V3_canScaleByMultiplyingWithAnIntOnTheRight (self):
        self.assertEqual(3 * tf.V3((1,3,2)), tf.V3((3,9,6)))

    def test_V3_canScaleByMultiplyingWithAFloat (self):
        self.assertEqual(tf.V3((1,3,2)) * 2.5, tf.V3((2.5,7.5,5.0)))

    def test_V3_canDivideV3s (self):
        x, y, z = (tf.V3((9,4,3)) / tf.V3((3,2,3))).xyz
        self.assertAlmostEqual(x, 3)
        self.assertAlmostEqual(y, 2)
        self.assertAlmostEqual(z, 1)

    def test_V3_divisionHasRightIdentity (self):
        self.assertEqual(tf.V3((9,4,3)) / tf.V3((1,1,1)), tf.V3((9,4,3)))

    def test_V3_cannotDivideByZero (self):
        self.assertRaises(ZeroDivisionError, lambda: tf.V3((1,3,5)) / tf.V3((0,0,0)))

    def test_V3_canBeDividedByAnInt (self):
        self.assertEqual(tf.V3((1,2,3)) / 2, tf.V3((0.5,1,1.5)))

    def test_V3_canBeDividedByAnFloat (self):
        self.assertEqual(tf.V3((1,2,3)) / 0.1, tf.V3((10,20,30)))

    def test_V3_magnitudeAtOriginIsZero (self):
        self.assertEqual(tf.V3((0,0,0)).mag(), 0)

    def test_V3_magnitudeAtX1Is1 (self):
        self.assertEqual(tf.V3((1,0,0)).mag(), 1)

    def test_V3_magnitudeAtY1Is1 (self):
        self.assertEqual(tf.V3((0,1,0)).mag(), 1)

    def test_V3_magnitudeAtZ1Is1 (self):
        self.assertEqual(tf.V3((0,0,1)).mag(), 1)

    def test_V3_magnitudeAtX1Y1Z1IsSqrt3 (self):
        self.assertEqual(tf.V3((1,1,1)).mag(), sqrt(3))

    def test_V3_unitIsIdempotentOnX1Y0Z0 (self):
        self.assertEqual(tf.V3((1,0,0)).unit(), tf.V3((1,0,0)))

    def test_V3_unitIsIdempotentOnX0Y1Z0 (self):
        self.assertEqual(tf.V3((0,1,0)).unit(), tf.V3((0,1,0)))

    def test_V3_unitIsIdempotentOnX0Y0Z1 (self):
        self.assertEqual(tf.V3((0,0,1)).unit(), tf.V3((0,0,1)))

    def test_V3_unitIsRecipOfSqrt3PerAxisOnX1Y1Z1 (self):
        self.assertEqual(tf.V3((1,1,1)).unit(), tf.V3((1.0/sqrt(3),1.0/sqrt(3),1.0/sqrt(3))))


class Test_v3Avg (unittest.TestCase):

    def test_v3Avg_emptyListYieldsEmptyList (self):
        self.assertEqual(tf.v3Avg([]), tf.V3([]))

    def test_v3Avg_singleListYieldsItsElement (self):
        self.assertEqual(tf.v3Avg([tf.V3((1,2,3))]), tf.V3((1,2,3)))

    def test_v3Avg_2ElementListFindsMidpoint (self):
        self.assertEqual(tf.v3Avg([tf.V3((1,2,3)),tf.V3((3,2,0))]), tf.V3((2,2,1.5)))

    def test_v3Avg_averagesManyElements (self):
        elems = [tf.V3((1,2,2)), tf.V3((3,1,3)), tf.V3((2,2,1)), tf.V3((3,1,2))]
        self.assertEqual(tf.v3Avg(elems), tf.V3((2.25,1.5,2.0)))


class Test_v3Mid (unittest.TestCase):

    def test_v3Mid_midpointOf2OriginsIsOrigin (self):
        o = tf.V3((0,0,0))
        self.assertEqual(tf.v3Mid(o)(o), o)

    def test_v3Mid_findsMidpointOf2PositivePoints (self):
        self.assertEqual(tf.v3Mid(tf.V3((2,3,1)))(tf.V3((2,0,3))), tf.V3((2,1.5,2)))

    def test_v3Mid_findsMidpointOf2NegativePoints (self):
        self.assertEqual(tf.v3Mid(tf.V3((-2,-3,-1)))(tf.V3((-2,-0,-3))), tf.V3((-2,-1.5,-2)))

    def test_v3Mid_midPointOfOriginAndX2Y2Z2IsX1Y1Z1 (self):
        self.assertEqual(tf.v3Mid(tf.V3((0,0,0)))(tf.V3((2,2,2))), tf.V3((1,1,1)))


# IMPURE

@attr('maya')
@unittest.skipUnless(hasMaya, "requires Maya")
class Test_pos (unittest.TestCase):

    def setUp (self):
        cmds.file(new=True, force=True)

    def test_pos_newTransformAtOrigin (self):
        loc = cmds.spaceLocator()[0]
        self.assertEqual(tf.pos(loc), (0,0,0))

    def test_pos_getsSetPos (self):
        loc = cmds.spaceLocator()[0]
        cmds.move(1, 2, 3, loc)
        self.assertEqual(tf.pos(loc), (1,2,3))

    def test_pos_getsLocalPos (self):
        loc = cmds.spaceLocator()[0]
        grp = cmds.group()
        cmds.move(1, 2, 3, grp)
        self.assertEqual(tf.pos(loc), (0,0,0))

    def test_pos_getsLocalSetPos (self):
        loc = cmds.spaceLocator()[0]
        cmds.move(2, -3, 1, loc)
        grp = cmds.group()
        cmds.move(1, 2, 3, grp)
        self.assertEqual(tf.pos(loc), (2,-3,1))


@attr('maya')
@unittest.skipUnless(hasMaya, "requires Maya")
class Test_setpos (unittest.TestCase):

    def setUp (self):
        cmds.file(new=True, force=True)

    def test_setpos_canSetPos (self):
        loc = cmds.spaceLocator()[0]
        tf.setpos(loc)((4,2,1))
        pos = tuple(cmds.xform(loc, query=True, translation=True))
        self.assertEqual(pos, (4,2,1))

    def test_setpos_returnsNone (self):
        loc = cmds.spaceLocator()[0]
        result = tf.setpos(loc)((4,2,1))
        self.assertEqual(result, None)


@attr('maya')
@unittest.skipUnless(hasMaya, "requires Maya")
class Test_wpos (unittest.TestCase):

    def setUp (self):
        cmds.file(new=True, force=True)

    def test_wpos_newTransformAtOrigin (self):
        loc = cmds.spaceLocator()[0]
        self.assertEqual(tf.wpos(loc), (0,0,0))

    def test_wpos_getsSetPos (self):
        loc = cmds.spaceLocator()[0]
        cmds.move(1, 2, 3, loc)
        self.assertEqual(tf.wpos(loc), (1,2,3))

    def test_wpos_getsWorldPosFromInsideMovedContainer (self):
        loc = cmds.spaceLocator()[0]
        grp = cmds.group()
        cmds.move(1, 2, 3, grp)
        self.assertEqual(tf.wpos(loc), (1,2,3))

    def test_wpos_getsWorldPosFromSetPosInsideMovedContainer (self):
        loc = cmds.spaceLocator()[0]
        cmds.move(2, -3, 1, loc)
        grp = cmds.group()
        cmds.move(1, 2, 3, grp)
        self.assertEqual(tf.wpos(loc), (3,-1,4))


@attr('maya')
@unittest.skipUnless(hasMaya, "requires Maya")
class Test_setwpos (unittest.TestCase):

    def setUp (self):
        cmds.file(new=True, force=True)

    def test_setwpos_canSetWSPos (self):
        loc = cmds.spaceLocator()[0]
        tf.setwpos(loc)((4,2,1))
        pos = tuple(cmds.xform(loc, query=True, translation=True))
        self.assertEqual(pos, (4,2,1))

    def test_setwpos_canSetWSPosInsideMovedContainer (self):
        loc = cmds.spaceLocator()[0]
        grp = cmds.group()
        cmds.move(1, 2, 3, grp)
        pos = tuple(cmds.xform(loc, query=True, worldSpace=True, translation=True))
        self.assertEqual(pos, (1,2,3))
        tf.setwpos(loc)((4,2,1))
        pos = tuple(cmds.xform(loc, query=True, worldSpace=True, translation=True))
        self.assertEqual(pos, (4,2,1))

    def test_setwpos_returnsNone (self):
        loc = cmds.spaceLocator()[0]
        result = tf.setwpos(loc)((4,2,1))
        self.assertEqual(result, None)


@attr('maya')
@unittest.skipUnless(hasMaya, "requires Maya")
class Test_rot (unittest.TestCase):

    def setUp (self):
        cmds.file(new=True, force=True)

    def test_rot_canGetRot (self):
        loc = cmds.spaceLocator()[0]
        cmds.xform(loc, rotation=(20,50,85))
        self.assertEqual(tf.rot(loc), (20,50,85))

    def test_rot_doesNotInerheritRotationOfContainer (self):
        loc = cmds.spaceLocator()[0]
        grp = cmds.group()
        cmds.xform(grp, rotation=(37,-23,14))
        self.assertEqual(tf.rot(loc), (0,0,0))


@attr('maya')
@unittest.skipUnless(hasMaya, "requires Maya")
class Test_setRot (unittest.TestCase):

    def setUp (self):
        cmds.file(new=True, force=True)

    def test_setRot_canSetRot (self):
        loc = cmds.spaceLocator()[0]
        tf.setrot(loc)((23,34,45))
        rot = cmds.xform(loc, query=True, rotation=True)

    def test_setRot_setsLocalRotationInRotatedContainer (self):
        loc = cmds.spaceLocator()[0]
        grp = cmds.group()
        cmds.xform(grp, rotation=(34,56,23))
        tf.setrot(loc)((10,23,34))
        rot = cmds.xform(loc, query=True, rotation=True)
        self.assertEqual(tf.rot(loc), (10,23,34))

    def test_setRot_returnsNone (self):
        loc = cmds.spaceLocator()[0]
        result = tf.setrot(loc)((55,98,-23))
        self.assertEqual(result, None)


@attr('maya')
@unittest.skipUnless(hasMaya, "requires Maya")
class Test_wrot (unittest.TestCase):

    def setUp (self):
        cmds.file(new=True, force=True)

    def test_wrot_newTransformAtOrigin (self):
        loc = cmds.spaceLocator()[0]
        self.assertEqual(tf.wrot(loc), (0,0,0))

    def test_wrot_getsSetRot (self):
        loc = cmds.spaceLocator()[0]
        cmds.rotate(10, 43, 49, loc)
        x, y, z = tf.wrot(loc)
        self.assertAlmostEqual(x, 10)
        self.assertAlmostEqual(y, 43)
        self.assertAlmostEqual(z, 49)

    def test_wrot_getsUnrotatedWorldRotFromInsideRotatedContainer (self):
        loc = cmds.spaceLocator()[0]
        grp = cmds.group()
        cmds.rotate(10, 11, 23, grp)
        x, y, z = tf.wrot(loc)
        self.assertAlmostEqual(x, 10)
        self.assertAlmostEqual(y, 11)
        self.assertAlmostEqual(z, 23)

    def test_wrot_getsWorldRotFromSetRotInsideMovedContainer (self):
        loc = cmds.spaceLocator()[0]
        cmds.rotate(90, -90, 270, loc)
        grp = cmds.group()
        cmds.rotate(0, -90, 180, grp)
        x, y, z = tf.wrot(loc)
        self.assertAlmostEqual(x, 360)
        self.assertAlmostEqual(y, -180)
        self.assertAlmostEqual(z, 180)


@attr('maya')
@unittest.skipUnless(hasMaya, "requires Maya")
class Test_setwrot (unittest.TestCase):

    def setUp (self):
        cmds.file(new=True, force=True)

    def test_setwrot_newTransformAtOrigin (self):
        loc = cmds.spaceLocator()[0]
        rot = tuple(cmds.xform(loc, query=True, rotation=True))
        self.assertEqual(rot, (0,0,0))

    def test_setwrot_canSetWSRotInsideRotatedContainer (self):
        loc = cmds.spaceLocator()[0]
        grp = cmds.group()
        cmds.rotate(-90, 90, -180, grp)
        x, y, z = tuple(cmds.xform(loc, query=True, worldSpace=True, rotation=True))
        self.assertAlmostEqual(x, 90)
        self.assertAlmostEqual(y, 90)
        self.assertAlmostEqual(z, 0)
        tf.setwrot(loc)((90,-90,180))
        x, y, z = tuple(cmds.xform(loc, query=True, worldSpace=True, rotation=True))
        self.assertAlmostEqual(x, -90)
        self.assertAlmostEqual(y, 270)
        self.assertAlmostEqual(z, 0)

    def test_setwrot_returnsNone (self):
        loc = cmds.spaceLocator()[0]
        result = tf.setwrot(loc)((4,2,1))
        self.assertEqual(result, None)


@attr('maya')
@unittest.skipUnless(hasMaya, "requires Maya")
class Test_posrot (unittest.TestCase):

    def test_posrot_getsTestObjectTransforms (self):
        loc = cmds.spaceLocator()[0]
        cmds.move(1, 2, 3)
        cmds.rotate(23, 43, 12)
        (tx, ty, tz), (rx, ry, rz) = tf.posrot(loc)
        self.assertAlmostEqual(tx, 1)
        self.assertAlmostEqual(ty, 2)
        self.assertAlmostEqual(tz, 3)
        self.assertAlmostEqual(rx, 23)
        self.assertAlmostEqual(ry, 43)
        self.assertAlmostEqual(rz, 12)

    def test_posrot_getsTestObjectTransformsRelativeToParent (self):
        loc = cmds.spaceLocator()[0]
        cmds.group()
        cmds.move(1, 2, 3)
        cmds.rotate(23, 43, 12)
        (tx, ty, tz), (rx, ry, rz) = tf.posrot(loc)
        self.assertAlmostEqual(tx, 0)
        self.assertAlmostEqual(ty, 0)
        self.assertAlmostEqual(tz, 0)
        self.assertAlmostEqual(rx, 0)
        self.assertAlmostEqual(ry, 0)
        self.assertAlmostEqual(rz, 0)


@attr('maya')
@unittest.skipUnless(hasMaya, "requires Maya")
class Test_wposrot (unittest.TestCase):

    def test_wposrot_getsTestObjectTransforms (self):
        loc = cmds.spaceLocator()[0]
        cmds.move(1, 2, 3)
        cmds.rotate(23, 43, 12)
        (tx, ty, tz), (rx, ry, rz) = tf.wposrot(loc)
        self.assertAlmostEqual(tx, 1)
        self.assertAlmostEqual(ty, 2)
        self.assertAlmostEqual(tz, 3)
        self.assertAlmostEqual(rx, 23)
        self.assertAlmostEqual(ry, 43)
        self.assertAlmostEqual(rz, 12)

    def test_wposrot_getsTestObjectTransformsRelativeToWorld (self):
        loc = cmds.spaceLocator()[0]
        cmds.group()
        cmds.move(1, 2, 3)
        cmds.rotate(23, 43, 12)
        (tx, ty, tz), (rx, ry, rz) = tf.wposrot(loc)
        self.assertAlmostEqual(tx, 1)
        self.assertAlmostEqual(ty, 2)
        self.assertAlmostEqual(tz, 3)
        self.assertAlmostEqual(rx, 23)
        self.assertAlmostEqual(ry, 43)
        self.assertAlmostEqual(rz, 12)

