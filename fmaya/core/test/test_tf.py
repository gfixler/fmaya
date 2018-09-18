import unittest
from nose.plugins.attrib import attr

from math import sqrt

try:
    import maya.cmds as cmds
except ImportError:
    print 'WARNING (%s): failed to load maya.cmds module.' % __file__

from .. import tf


# PURE

class Test_xyzAdd (unittest.TestCase):

    def test_xyzAdd_identities (self):
        self.assertEquals(tf.xyzAdd((0,0,0))((0,0,0)), (0,0,0))

    def test_xyzAdd_leftIdentity (self):
        self.assertEquals(tf.xyzAdd((0,0,0))((2,1,5)), (2,1,5))

    def test_xyzAdd_rightIdentity (self):
        self.assertEquals(tf.xyzAdd((3,2,5))((0,0,0)), (3,2,5))

    def test_xyzAdd_positives (self):
        self.assertEquals(tf.xyzAdd((3,2,5))((2,1,1)), (5,3,6))

    def test_xyzAdd_negatives (self):
        self.assertEquals(tf.xyzAdd((-2,-3,-1))((-2,-1,-3)), (-4,-4,-4))

    def test_xyzAdd_negativesAndPositives (self):
        self.assertEquals(tf.xyzAdd((-2,3,1))((2,-1,3)), (0,2,4))


class Test_xyzSub (unittest.TestCase):

    def test_xyzSub_identities (self):
        self.assertEquals(tf.xyzSub((0,0,0))((0,0,0)), (0,0,0))

    def test_xyzSub_noLeftIdentity (self):
        self.assertEquals(tf.xyzSub((0,0,0))((2,1,5)), (-2,-1,-5))

    def test_xyzSub_rightIdentity (self):
        self.assertEquals(tf.xyzSub((3,2,5))((0,0,0)), (3,2,5))

    def test_xyzSub_positives (self):
        self.assertEquals(tf.xyzSub((3,2,5))((2,1,1)), (1,1,4))

    def test_xyzSub_negatives (self):
        self.assertEquals(tf.xyzSub((-2,-3,-1))((-2,-1,-3)), (0,-2,2))

    def test_xyzSub_negativesAndPositives (self):
        self.assertEquals(tf.xyzSub((-2,3,1))((2,-1,3)), (-4,4,-2))


class Test_xyzMul (unittest.TestCase):

    def test_xyzMul_zeroes (self):
        self.assertEquals(tf.xyzMul((0,0,0))((0,0,0)), (0,0,0))

    def test_xyzMul_identities (self):
        self.assertEquals(tf.xyzMul((1,1,1))((1,1,1)), (1,1,1))

    def test_xyzMul_leftIdentity (self):
        self.assertEquals(tf.xyzMul((1,1,1))((2,1,5)), (2,1,5))

    def test_xyzMul_rightIdentity (self):
        self.assertEquals(tf.xyzMul((3,2,5))((1,1,1)), (3,2,5))

    def test_xyzMul_positives (self):
        self.assertEquals(tf.xyzMul((3,2,5))((2,1,1)), (6,2,5))

    def test_xyzMul_negatives (self):
        self.assertEquals(tf.xyzMul((-2,-3,-1))((-2,-1,-3)), (4,3,3))

    def test_xyzMul_negativesAndPositives (self):
        self.assertEquals(tf.xyzMul((-2,3,1))((2,-1,3)), (-4,-3,3))


class Test_xyzDiv (unittest.TestCase):

    def test_xyzDiv_dividingByZeroesRaises (self):
        self.assertRaises(ZeroDivisionError, lambda: tf.xyzDiv((1,1,1))((0,0,0)))

    def test_xyzDiv_identities (self):
        self.assertEquals(tf.xyzDiv((1,1,1))((1,1,1)), (1.0,1.0,1.0))

    def test_xyzDiv_noLeftIdentity (self):
        self.assertEquals(tf.xyzDiv((1,1,1))((2,1,5)), (0.5,1.0,0.2))

    def test_xyzDiv_rightIdentity (self):
        self.assertEquals(tf.xyzDiv((3,2,5))((1,1,1)), (3.0,2.0,5.0))

    def test_xyzDiv_allResultsPreservedAsOrPromotedToFloats (self):
        x, y, z = tf.xyzDiv((9,7,13))((3,3,4))
        self.assertTrue(type(x) == float and type(y) == float and type(z) == float)

    def test_xyzDiv_positives (self):
        self.assertEquals(tf.xyzDiv((3,2,5))((2,1,1)), (1.5,2.0,5.0))

    def test_xyzDiv_negatives (self):
        self.assertEquals(tf.xyzDiv((-2,-3,-3))((-2,-1,-3)), (1.0,3.0,1.0))

    def test_xyzDiv_negativesAndPositives (self):
        self.assertEquals(tf.xyzDiv((-2,3,3))((2,-1,3)), (-1.0,-3.0,1.0))


class Test_xyzScale (unittest.TestCase):

    def test_xyzScale_zeroZeroOut (self):
        self.assertEquals(tf.xyzScale(0)((-2,3,3)), (0,0,0))

    def test_xyzScale_hasIdentity (self):
        self.assertEquals(tf.xyzScale(1)((-2,3,1)), (-2,3,1))

    def test_xyzScale_scales (self):
        self.assertEquals(tf.xyzScale(3)((-2,3,1)), (-6,9,3))

    def test_xyzScale_inverseScales (self):
        self.assertEquals(tf.xyzScale(-1)((-2,3,1)), (2,-3,-1))


class Test_xyzSum (unittest.TestCase):

    def test_xyzSum_preservesIdentity (self):
        self.assertEquals(tf.xyzSum([]), (0,0,0))

    def test_xyzSum_keepsSingletonElement (self):
        self.assertEquals(tf.xyzSum([(2,-1,3)]), (2,-1,3))

    def test_xyzSum_sumsElements (self):
        self.assertEquals(tf.xyzSum([(2,-1,3),(1,1,2),(-3,2,-2),(-3,-1,2)]), (-3,1,5))


class Test_xyzAvg (unittest.TestCase):

    def test_xyzAvg_preservesIdentity (self):
        self.assertEquals(tf.xyzAvg([]), (0,0,0))

    def test_xyzAvg_keepsSingletonElement (self):
        self.assertEquals(tf.xyzAvg([(2,1,-3)]), (2,1,-3))

    def test_xyzAvg_sameTriplesAverageToThemselves (self):
        (x,y,z) = tf.xyzAvg([(1,2,3)] * 35)
        self.assertAlmostEquals(x, 1)
        self.assertAlmostEquals(y, 2)
        self.assertAlmostEquals(z, 3)

    def test_xyzAvg_averagesSomeIntegers (self):
        self.assertEquals(tf.xyzAvg([(1,2,3),(2,3,1),(3,4,-3),(2,3,-1)]), (2,3,0))


class Test_xyzDist (unittest.TestCase):

    def test_xyzDist_zeroWhenBothPointsAtOrigin (self):
        self.assertEquals(tf.xyzDist((0,0,0))((0,0,0)), 0.0)

    def test_xyzDist_zeroWhenBothPointsMatchAllPositive (self):
        self.assertEquals(tf.xyzDist((1,3,2))((1,3,2)), 0.0)

    def test_xyzDist_zeroWhenBothPointsMatchAllPositive (self):
        self.assertEquals(tf.xyzDist((-2,-4,-1))((-2,-4,-1)), 0.0)

    def test_xyzDist_getsLengthDownXAxisOnly (self):
        self.assertEquals(tf.xyzDist((1,2,3))((6,2,3)), 5.0)

    def test_xyzDist_getsLengthDownYAxisOnly (self):
        self.assertEquals(tf.xyzDist((1,2,3))((1,12,3)), 10.0)

    def test_xyzDist_getsLengthDownZAxisOnly (self):
        self.assertEquals(tf.xyzDist((1,2,3))((1,2,18)), 15.0)

    def test_xyzDist_345TriangleInXYPlane (self):
        self.assertEquals(tf.xyzDist((0,0,0))((3,4,0)), 5.0)

    def test_xyzDist_345TriangleInYZPlane (self):
        self.assertEquals(tf.xyzDist((0,0,0))((0,4,3)), 5.0)


class Test_xyzHypot (unittest.TestCase):

    def test_xyzHypot_zeroAtOrigin (self):
        self.assertEquals(tf.xyzHypot((0,0,0)), 0.0)

    def test_xyzHypot_345TriangleInXYPlane (self):
        self.assertEquals(tf.xyzHypot((3,4,0)), 5.0)

    def test_xyzHypot_345TriangleInXZPlane (self):
        self.assertEquals(tf.xyzHypot((3,0,4)), 5.0)

    def test_xyzHypot_345TriangleInYZPlane (self):
        self.assertEquals(tf.xyzHypot((0,3,4)), 5.0)

    def test_xyzHypot_unitCubeDiagonalEqualsSquareRootOf3 (self):
        self.assertEquals(tf.xyzHypot((1,1,1)), sqrt(3))


class Test_xyzUnit (unittest.TestCase):

    def test_xyzUnit_preservesXIdentity (self):
        self.assertEquals(tf.xyzUnit((1,0,0)), (1,0,0))

    def test_xyzUnit_preservesYIdentity (self):
        self.assertEquals(tf.xyzUnit((0,1,0)), (0,1,0))

    def test_xyzUnit_preservesZIdentity (self):
        self.assertEquals(tf.xyzUnit((0,0,1)), (0,0,1))

    def test_xyzUnit_shrinksAlongX (self):
        self.assertEquals(tf.xyzUnit((5,0,0)), (1,0,0))

    def test_xyzUnit_expandsAlongX (self):
        self.assertEquals(tf.xyzUnit((0.1,0,0)), (1,0,0))

    def test_xyzUnit_shrinksAlongY (self):
        self.assertEquals(tf.xyzUnit((0,5,0)), (0,1,0))

    def test_xyzUnit_expandsAlongY (self):
        self.assertEquals(tf.xyzUnit((0,0.1,0)), (0,1,0))

    def test_xyzUnit_shrinksAlongZ (self):
        self.assertEquals(tf.xyzUnit((0,0,5)), (0,0,1))

    def test_xyzUnit_expandsAlongZ (self):
        self.assertEquals(tf.xyzUnit((0,0,0.1)), (0,0,1))

    def test_xyzUnit_hypotOfResultIs1 (self):
        self.assertEquals(tf.xyzHypot(tf.xyzUnit((23.3,-12.8,4.2))), 1.0)


class Test_V3 (unittest.TestCase):

    def test_V3_canInstantitateAndReadDefaultXYZValues (self):
        v3 = tf.V3()
        self.assertEquals(v3.xyz, (0,0,0))

    def test_V3_canInstantiateWithXYZValues (self):
        v3 = tf.V3((3,7,4))
        self.assertEquals(v3.xyz, (3,7,4))

    def test_V3_convertsToTupleUnderTheHood (self):
        v3 = tf.V3([1,2,3])
        self.assertEquals(v3.xyz, (1,2,3))

    def test_V3_canGetXValue (self):
        v3 = tf.V3((2,3,4))
        self.assertEquals(v3.x, 2)

    def test_V3_canSetXValue (self):
        v3 = tf.V3((5,6,7))
        v3.x = 9
        self.assertEquals(v3.xyz, (9,6,7))

    def test_V3_canGetYValue (self):
        v3 = tf.V3((2,3,4))
        self.assertEquals(v3.y, 3)

    def test_V3_canSetXValue (self):
        v3 = tf.V3((5,6,7))
        v3.y = 11
        self.assertEquals(v3.xyz, (5,11,7))

    def test_V3_canGetZValue (self):
        v3 = tf.V3((2,3,4))
        self.assertEquals(v3.z, 4)

    def test_V3_canSetXValue (self):
        v3 = tf.V3((5,6,7))
        v3.z = 13
        self.assertEquals(v3.xyz, (5,6,13))

    def test_V3_reprIncluesV3Tag (self):
        v3 = tf.V3((2,4,8))
        self.assertEquals(repr(v3), "V3 (2, 4, 8)")

    def test_V3_equality (self):
        self.assertEquals(tf.V3((1,2,3)), tf.V3((1,2,3)))

    def test_V3_inequality (self):
        self.assertNotEqual(tf.V3((2,2,3)), tf.V3((1,2,3)))

    def test_V3_canAddV3s (self):
        self.assertEquals(tf.V3((-2,3,1)) + tf.V3((1,2,3)), tf.V3((-1,5,4)))

    def test_V3_additionHasLeftIdentity (self):
        self.assertEquals(tf.V3((0,0,0)) + tf.V3((-2,3,1)), tf.V3((-2,3,1)))

    def test_V3_additionHasRightIdentity (self):
        self.assertEquals(tf.V3((-2,3,1)) + tf.V3((0,0,0)), tf.V3((-2,3,1)))

    def test_V3_canAddIntOnRight (self):
        self.assertEquals(tf.V3((3,1,2)) + 5, tf.V3((8,6,7)))

    def test_V3_canAddIntOnLeft (self):
        self.assertEquals(3 + tf.V3((3,1,2)), tf.V3((6,4,5)))

    def test_V3_canSumV3s (self):
        self.assertEquals(sum([tf.V3((1,2,3)),tf.V3((3,2,2)),tf.V3((3,2,2))]), tf.V3((7,6,7)))

    def test_V3_canReduceV3sWithAddition (self):
        v3s = [tf.V3((1,2,3)), tf.V3((2,1,1)), tf.V3((-2,-3,1)), tf.V3((-2,2,3))]
        result = reduce(lambda x, y: x + y, v3s)
        self.assertEquals(result, tf.V3((-1,2,8)))

    def test_V3_canSubtractV3s (self):
        self.assertEquals(tf.V3((2,4,1)) - tf.V3((-1,3,2)), tf.V3((3,1,-1)))

    def test_V3_subtractionHasRightIdentity (self):
        self.assertEquals(tf.V3((3,1,2)) - tf.V3((0,0,0)), tf.V3((3,1,2)))

    def test_V3_canMultiplyV3s (self):
        self.assertEquals(tf.V3((1,2,3)) * tf.V3((2,3,1)), tf.V3((2,6,3)))

    def test_V3_multiplicationHasLeftIdentity (self):
        self.assertEquals(tf.V3((1,1,1)) * tf.V3((-2,3,1)), tf.V3((-2,3,1)))

    def test_V3_multiplicationHasRightIdentity (self):
        self.assertEquals(tf.V3((-2,3,1)) * tf.V3((1,1,1)), tf.V3((-2,3,1)))

    def test_V3_canReduceV3sWithMultiplication (self):
        v3s = [tf.V3((1,2,3)), tf.V3((2,1,1)), tf.V3((-2,-3,1)), tf.V3((-2,2,3))]
        result = reduce(lambda x, y: x * y, v3s)
        self.assertEquals(result, tf.V3((8,-12,9)))

    def test_V3_canScaleByMultiplyingWithAnIntOnTheLeft (self):
        self.assertEquals(tf.V3((1,3,2)) * 3, tf.V3((3,9,6)))

    def test_V3_canScaleByMultiplyingWithAnIntOnTheRight (self):
        self.assertEquals(3 * tf.V3((1,3,2)), tf.V3((3,9,6)))

    def test_V3_canScaleByMultiplyingWithAFloat (self):
        self.assertEquals(tf.V3((1,3,2)) * 2.5, tf.V3((2.5,7.5,5.0)))

    def test_V3_canDivideV3s (self):
        x, y, z = (tf.V3((9,4,3)) / tf.V3((3,2,3))).xyz
        self.assertAlmostEquals(x, 3)
        self.assertAlmostEquals(y, 2)
        self.assertAlmostEquals(z, 1)

    def test_V3_divisionHasRightIdentity (self):
        self.assertEquals(tf.V3((9,4,3)) / tf.V3((1,1,1)), tf.V3((9,4,3)))

    def test_V3_cannotDivideByZero (self):
        self.assertRaises(ZeroDivisionError, lambda: tf.V3((1,3,5)) / tf.V3((0,0,0)))

    def test_V3_canBeDividedByAnInt (self):
        self.assertEquals(tf.V3((1,2,3)) / 2, tf.V3((0.5,1,1.5)))

    def test_V3_canBeDividedByAnFloat (self):
        self.assertEquals(tf.V3((1,2,3)) / 0.1, tf.V3((10,20,30)))

    def test_V3_magnitudeAtOriginIsZero (self):
        self.assertEquals(tf.V3((0,0,0)).mag(), 0)

    def test_V3_magnitudeAtX1Is1 (self):
        self.assertEquals(tf.V3((1,0,0)).mag(), 1)

    def test_V3_magnitudeAtY1Is1 (self):
        self.assertEquals(tf.V3((0,1,0)).mag(), 1)

    def test_V3_magnitudeAtZ1Is1 (self):
        self.assertEquals(tf.V3((0,0,1)).mag(), 1)

    def test_V3_magnitudeAtX1Y1Z1IsSqrt3 (self):
        self.assertEquals(tf.V3((1,1,1)).mag(), sqrt(3))

    def test_V3_unitIsIdempotentOnX1Y0Z0 (self):
        self.assertEquals(tf.V3((1,0,0)).unit(), tf.V3((1,0,0)))

    def test_V3_unitIsIdempotentOnX0Y1Z0 (self):
        self.assertEquals(tf.V3((0,1,0)).unit(), tf.V3((0,1,0)))

    def test_V3_unitIsIdempotentOnX0Y0Z1 (self):
        self.assertEquals(tf.V3((0,0,1)).unit(), tf.V3((0,0,1)))

    def test_V3_unitIsRecipOfSqrt3PerAxisOnX1Y1Z1 (self):
        self.assertEquals(tf.V3((1,1,1)).unit(), tf.V3((1.0/sqrt(3),1.0/sqrt(3),1.0/sqrt(3))))


class Test_v3Avg (unittest.TestCase):

    def test_v3Avg_emptyListYieldsEmptyList (self):
        self.assertEquals(tf.v3Avg([]), tf.V3([]))

    def test_v3Avg_singleListYieldsItsElement (self):
        self.assertEquals(tf.v3Avg([tf.V3((1,2,3))]), tf.V3((1,2,3)))

    def test_v3Avg_2ElementListFindsMidpoint (self):
        self.assertEquals(tf.v3Avg([tf.V3((1,2,3)),tf.V3((3,2,0))]), tf.V3((2,2,1.5)))

    def test_v3Avg_averagesManyElements (self):
        elems = [tf.V3((1,2,2)), tf.V3((3,1,3)), tf.V3((2,2,1)), tf.V3((3,1,2))]
        self.assertEquals(tf.v3Avg(elems), tf.V3((2.25,1.5,2.0)))


class Test_v3Mid (unittest.TestCase):

    def test_v3Mid_midpointOf2OriginsIsOrigin (self):
        o = tf.V3((0,0,0))
        self.assertEquals(tf.v3Mid(o)(o), o)

    def test_v3Mid_findsMidpointOf2PositivePoints (self):
        self.assertEquals(tf.v3Mid(tf.V3((2,3,1)))(tf.V3((2,0,3))), tf.V3((2,1.5,2)))

    def test_v3Mid_findsMidpointOf2NegativePoints (self):
        self.assertEquals(tf.v3Mid(tf.V3((-2,-3,-1)))(tf.V3((-2,-0,-3))), tf.V3((-2,-1.5,-2)))

    def test_v3Mid_midPointOfOriginAndX2Y2Z2IsX1Y1Z1 (self):
        self.assertEquals(tf.v3Mid(tf.V3((0,0,0)))(tf.V3((2,2,2))), tf.V3((1,1,1)))


# IMPURE

@attr('maya')
class Test_pos (unittest.TestCase):

    def setUp (self):
        cmds.file(new=True, force=True)

    def test_pos_newTransformAtOrigin (self):
        loc = cmds.spaceLocator()[0]
        self.assertEquals(tf.pos(loc), (0,0,0))

    def test_pos_getsSetPos (self):
        loc = cmds.spaceLocator()[0]
        cmds.move(1, 2, 3, loc)
        self.assertEquals(tf.pos(loc), (1,2,3))

    def test_pos_getsLocalPos (self):
        loc = cmds.spaceLocator()[0]
        grp = cmds.group()
        cmds.move(1, 2, 3, grp)
        self.assertEquals(tf.pos(loc), (0,0,0))

    def test_pos_getsLocalSetPos (self):
        loc = cmds.spaceLocator()[0]
        cmds.move(2, -3, 1, loc)
        grp = cmds.group()
        cmds.move(1, 2, 3, grp)
        self.assertEquals(tf.pos(loc), (2,-3,1))


@attr('maya')
class Test_setPos (unittest.TestCase):

    def setUp (self):
        cmds.file(new=True, force=True)

    def test_setPos_canSetPos (self):
        loc = cmds.spaceLocator()[0]
        tf.setPos(loc)((4,2,1))
        pos = tuple(cmds.xform(loc, query=True, translation=True))
        self.assertEquals(pos, (4,2,1))

    def test_setPos_returnsNone (self):
        loc = cmds.spaceLocator()[0]
        result = tf.setPos(loc)((4,2,1))
        self.assertEquals(result, None)


@attr('maya')
class Test_wpos (unittest.TestCase):

    def setUp (self):
        cmds.file(new=True, force=True)

    def test_wpos_newTransformAtOrigin (self):
        loc = cmds.spaceLocator()[0]
        self.assertEquals(tf.wpos(loc), (0,0,0))

    def test_wpos_getsSetPos (self):
        loc = cmds.spaceLocator()[0]
        cmds.move(1, 2, 3, loc)
        self.assertEquals(tf.wpos(loc), (1,2,3))

    def test_wpos_getsWorldPosFromInsideMovedContainer (self):
        loc = cmds.spaceLocator()[0]
        grp = cmds.group()
        cmds.move(1, 2, 3, grp)
        self.assertEquals(tf.wpos(loc), (1,2,3))

    def test_wpos_getsWorldPosFromSetPosInsideMovedContainer (self):
        loc = cmds.spaceLocator()[0]
        cmds.move(2, -3, 1, loc)
        grp = cmds.group()
        cmds.move(1, 2, 3, grp)
        self.assertEquals(tf.wpos(loc), (3,-1,4))


@attr('maya')
class Test_setwpos (unittest.TestCase):

    def setUp (self):
        cmds.file(new=True, force=True)

    def test_setwpos_canSetWSPos (self):
        loc = cmds.spaceLocator()[0]
        tf.setwpos(loc)((4,2,1))
        pos = tuple(cmds.xform(loc, query=True, translation=True))
        self.assertEquals(pos, (4,2,1))

    def test_setwpos_canSetWSPosInsideMovedContainer (self):
        loc = cmds.spaceLocator()[0]
        grp = cmds.group()
        cmds.move(1, 2, 3, grp)
        pos = tuple(cmds.xform(loc, query=True, worldSpace=True, translation=True))
        self.assertEquals(pos, (1,2,3))
        tf.setwpos(loc)((4,2,1))
        pos = tuple(cmds.xform(loc, query=True, worldSpace=True, translation=True))
        self.assertEquals(pos, (4,2,1))

    def test_setwpos_returnsNone (self):
        loc = cmds.spaceLocator()[0]
        result = tf.setwpos(loc)((4,2,1))
        self.assertEquals(result, None)


@attr('maya')
class Test_rot (unittest.TestCase):

    def setUp (self):
        cmds.file(new=True, force=True)

    def test_rot_canGetRot (self):
        loc = cmds.spaceLocator()[0]
        cmds.xform(loc, rotation=(20,50,85))
        self.assertEquals(tf.rot(loc), (20,50,85))

    def test_rot_doesNotInerheritRotationOfContainer (self):
        loc = cmds.spaceLocator()[0]
        grp = cmds.group()
        cmds.xform(grp, rotation=(37,-23,14))
        self.assertEquals(tf.rot(loc), (0,0,0))


@attr('maya')
class Test_setRot (unittest.TestCase):

    def setUp (self):
        cmds.file(new=True, force=True)

    def test_setRot_canSetRot (self):
        loc = cmds.spaceLocator()[0]
        tf.setRot(loc)((23,34,45))
        rot = cmds.xform(loc, query=True, rotation=True)

    def test_setRot_setsLocalRotationInRotatedContainer (self):
        loc = cmds.spaceLocator()[0]
        grp = cmds.group()
        cmds.xform(grp, rotation=(34,56,23))
        tf.setRot(loc)((10,23,34))
        rot = cmds.xform(loc, query=True, rotation=True)
        self.assertEquals(tf.rot(loc), (10,23,34))

    def test_setRot_returnsNone (self):
        loc = cmds.spaceLocator()[0]
        result = tf.setRot(loc)((55,98,-23))
        self.assertEquals(result, None)


@attr('maya')
class Test_wrot (unittest.TestCase):

    def setUp (self):
        cmds.file(new=True, force=True)

    def test_wrot_newTransformAtOrigin (self):
        loc = cmds.spaceLocator()[0]
        self.assertEquals(tf.wrot(loc), (0,0,0))

    def test_wrot_getsSetRot (self):
        loc = cmds.spaceLocator()[0]
        cmds.rotate(10, 43, 49, loc)
        x, y, z = tf.wrot(loc)
        self.assertAlmostEquals(x, 10)
        self.assertAlmostEquals(y, 43)
        self.assertAlmostEquals(z, 49)

    def test_wrot_getsUnrotatedWorldRotFromInsideRotatedContainer (self):
        loc = cmds.spaceLocator()[0]
        grp = cmds.group()
        cmds.rotate(10, 11, 23, grp)
        x, y, z = tf.wrot(loc)
        self.assertAlmostEquals(x, 10)
        self.assertAlmostEquals(y, 11)
        self.assertAlmostEquals(z, 23)

    def test_wrot_getsWorldRotFromSetRotInsideMovedContainer (self):
        loc = cmds.spaceLocator()[0]
        cmds.rotate(90, -90, 270, loc)
        grp = cmds.group()
        cmds.rotate(0, -90, 180, grp)
        x, y, z = tf.wrot(loc)
        self.assertAlmostEquals(x, 360)
        self.assertAlmostEquals(y, -180)
        self.assertAlmostEquals(z, 180)


@attr('maya')
class Test_setwrot (unittest.TestCase):

    def setUp (self):
        cmds.file(new=True, force=True)

    def test_setwrot_newTransformAtOrigin (self):
        loc = cmds.spaceLocator()[0]
        rot = tuple(cmds.xform(loc, query=True, rotation=True))
        self.assertEquals(rot, (0,0,0))

    def test_setwrot_canSetWSRotInsideRotatedContainer (self):
        loc = cmds.spaceLocator()[0]
        grp = cmds.group()
        cmds.rotate(-90, 90, -180, grp)
        x, y, z = tuple(cmds.xform(loc, query=True, worldSpace=True, rotation=True))
        self.assertAlmostEquals(x, 90)
        self.assertAlmostEquals(y, 90)
        self.assertAlmostEquals(z, 0)
        tf.setwrot(loc)((90,-90,180))
        x, y, z = tuple(cmds.xform(loc, query=True, worldSpace=True, rotation=True))
        self.assertAlmostEquals(x, -90)
        self.assertAlmostEquals(y, 270)
        self.assertAlmostEquals(z, 0)

    def test_setwrot_returnsNone (self):
        loc = cmds.spaceLocator()[0]
        result = tf.setwrot(loc)((4,2,1))
        self.assertEquals(result, None)


@attr('maya')
class Test_posrot (unittest.TestCase):

    def test_posrot_getsTestObjectTransforms (self):
        loc = cmds.spaceLocator()[0]
        cmds.move(1, 2, 3)
        cmds.rotate(23, 43, 12)
        (tx, ty, tz), (rx, ry, rz) = tf.posrot(loc)
        self.assertAlmostEquals(tx, 1)
        self.assertAlmostEquals(ty, 2)
        self.assertAlmostEquals(tz, 3)
        self.assertAlmostEquals(rx, 23)
        self.assertAlmostEquals(ry, 43)
        self.assertAlmostEquals(rz, 12)

    def test_posrot_getsTestObjectTransformsRelativeToParent (self):
        loc = cmds.spaceLocator()[0]
        cmds.group()
        cmds.move(1, 2, 3)
        cmds.rotate(23, 43, 12)
        (tx, ty, tz), (rx, ry, rz) = tf.posrot(loc)
        self.assertAlmostEquals(tx, 0)
        self.assertAlmostEquals(ty, 0)
        self.assertAlmostEquals(tz, 0)
        self.assertAlmostEquals(rx, 0)
        self.assertAlmostEquals(ry, 0)
        self.assertAlmostEquals(rz, 0)


