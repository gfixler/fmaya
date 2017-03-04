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
        v3a = tf.V3((1,2,3))
        v3b = tf.V3((-2,3,1))
        self.assertEquals(v3a + v3b, tf.V3((-1,5,4)))

    def test_V3_additionHasLeftIdentity (self):
        v3a = tf.V3((0,0,0))
        v3b = tf.V3((-2,3,1))
        self.assertEquals(v3a + v3b, tf.V3((-2,3,1)))

    def test_V3_additionHasRightIdentity (self):
        v3a = tf.V3((-2,3,1))
        v3b = tf.V3((0,0,0))
        self.assertEquals(v3a + v3b, tf.V3((-2,3,1)))

    def test_V3_canReduceV3sWithAddition (self):
        v3s = [tf.V3((1,2,3)), tf.V3((2,1,1)), tf.V3((-2,-3,1)), tf.V3((-2,2,3))]
        result = reduce(lambda x, y: x + y, v3s)
        self.assertEquals(result, tf.V3((-1,2,8)))


# IMPURE

@attr('maya')
class Test_getPos (unittest.TestCase):

    def setUp (self):
        cmds.file(new=True, force=True)

    def test_getPos_newTransformAtOrigin (self):
        loc = cmds.spaceLocator()[0]
        self.assertEquals(tf.getPos(loc), (0,0,0))

    def test_getPos_getsSetPos (self):
        loc = cmds.spaceLocator()[0]
        cmds.move(1, 2, 3, loc)
        self.assertEquals(tf.getPos(loc), (1,2,3))

    def test_getPos_getsLocalPos (self):
        loc = cmds.spaceLocator()[0]
        grp = cmds.group()
        cmds.move(1, 2, 3, grp)
        self.assertEquals(tf.getPos(loc), (0,0,0))

    def test_getPos_getsLocalSetPos (self):
        loc = cmds.spaceLocator()[0]
        cmds.move(2, -3, 1, loc)
        grp = cmds.group()
        cmds.move(1, 2, 3, grp)
        self.assertEquals(tf.getPos(loc), (2,-3,1))


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
class Test_getWSPos (unittest.TestCase):

    def setUp (self):
        cmds.file(new=True, force=True)

    def test_getWSPos_newTransformAtOrigin (self):
        loc = cmds.spaceLocator()[0]
        self.assertEquals(tf.getWSPos(loc), (0,0,0))

    def test_getWSPos_getsSetPos (self):
        loc = cmds.spaceLocator()[0]
        cmds.move(1, 2, 3, loc)
        self.assertEquals(tf.getWSPos(loc), (1,2,3))

    def test_getWSPos_getsWorldPosFromInsideMovedContainer (self):
        loc = cmds.spaceLocator()[0]
        grp = cmds.group()
        cmds.move(1, 2, 3, grp)
        self.assertEquals(tf.getWSPos(loc), (1,2,3))

    def test_getWSPos_getsWorldPosFromSetPosInsideMovedContainer (self):
        loc = cmds.spaceLocator()[0]
        cmds.move(2, -3, 1, loc)
        grp = cmds.group()
        cmds.move(1, 2, 3, grp)
        self.assertEquals(tf.getWSPos(loc), (3,-1,4))


@attr('maya')
class Test_setWSPos (unittest.TestCase):

    def setUp (self):
        cmds.file(new=True, force=True)

    def test_setWSPos_canSetWSPos (self):
        loc = cmds.spaceLocator()[0]
        tf.setWSPos(loc)((4,2,1))
        pos = tuple(cmds.xform(loc, query=True, translation=True))
        self.assertEquals(pos, (4,2,1))

    def test_setWSPos_canSetWSPosInsideMovedContainer (self):
        loc = cmds.spaceLocator()[0]
        grp = cmds.group()
        cmds.move(1, 2, 3, grp)
        pos = tuple(cmds.xform(loc, query=True, worldSpace=True, translation=True))
        self.assertEquals(pos, (1,2,3))
        tf.setWSPos(loc)((4,2,1))
        pos = tuple(cmds.xform(loc, query=True, worldSpace=True, translation=True))
        self.assertEquals(pos, (4,2,1))

    def test_setWSPos_returnsNone (self):
        loc = cmds.spaceLocator()[0]
        result = tf.setWSPos(loc)((4,2,1))
        self.assertEquals(result, None)


@attr('maya')
class Test_getRot (unittest.TestCase):

    def setUp (self):
        cmds.file(new=True, force=True)

    def test_getRot_canGetRot (self):
        loc = cmds.spaceLocator()[0]
        cmds.xform(loc, rotation=(20,50,85))
        self.assertEquals(tf.getRot(loc), (20,50,85))

    def test_getRot_doesNotInerheritRotationOfContainer (self):
        loc = cmds.spaceLocator()[0]
        grp = cmds.group()
        cmds.xform(grp, rotation=(37,-23,14))
        self.assertEquals(tf.getRot(loc), (0,0,0))


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
        self.assertEquals(tf.getRot(loc), (10,23,34))

    def test_setRot_returnsNone (self):
        loc = cmds.spaceLocator()[0]
        result = tf.setRot(loc)((55,98,-23))
        self.assertEquals(result, None)


@attr('maya')
class Test_getWSRot (unittest.TestCase):

    def setUp (self):
        cmds.file(new=True, force=True)

    def test_getWSRot_newTransformAtOrigin (self):
        loc = cmds.spaceLocator()[0]
        self.assertEquals(tf.getWSRot(loc), (0,0,0))

    def test_getWSRot_getsSetRot (self):
        loc = cmds.spaceLocator()[0]
        cmds.rotate(10, 43, 49, loc)
        x, y, z = tf.getWSRot(loc)
        self.assertAlmostEquals(x, 10)
        self.assertAlmostEquals(y, 43)
        self.assertAlmostEquals(z, 49)

    def test_getWSRot_getsUnrotatedWorldRotFromInsideRotatedContainer (self):
        loc = cmds.spaceLocator()[0]
        grp = cmds.group()
        cmds.rotate(10, 11, 23, grp)
        x, y, z = tf.getWSRot(loc)
        self.assertAlmostEquals(x, 10)
        self.assertAlmostEquals(y, 11)
        self.assertAlmostEquals(z, 23)

    def test_getWSRot_getsWorldRotFromSetRotInsideMovedContainer (self):
        loc = cmds.spaceLocator()[0]
        cmds.rotate(90, -90, 270, loc)
        grp = cmds.group()
        cmds.rotate(0, -90, 180, grp)
        x, y, z = tf.getWSRot(loc)
        self.assertAlmostEquals(x, 360)
        self.assertAlmostEquals(y, -180)
        self.assertAlmostEquals(z, 180)


@attr('maya')
class Test_setWSRot (unittest.TestCase):

    def setUp (self):
        cmds.file(new=True, force=True)

    def test_setWSRot_newTransformAtOrigin (self):
        loc = cmds.spaceLocator()[0]
        rot = tuple(cmds.xform(loc, query=True, rotation=True))
        self.assertEquals(rot, (0,0,0))

    def test_setWSRot_canSetWSRotInsideRotatedContainer (self):
        loc = cmds.spaceLocator()[0]
        grp = cmds.group()
        cmds.rotate(-90, 90, -180, grp)
        x, y, z = tuple(cmds.xform(loc, query=True, worldSpace=True, rotation=True))
        self.assertAlmostEquals(x, 90)
        self.assertAlmostEquals(y, 90)
        self.assertAlmostEquals(z, 0)
        tf.setWSRot(loc)((90,-90,180))
        x, y, z = tuple(cmds.xform(loc, query=True, worldSpace=True, rotation=True))
        self.assertAlmostEquals(x, 270)
        self.assertAlmostEquals(y, 270)
        self.assertAlmostEquals(z, 0)

    def test_setWSRot_returnsNone (self):
        loc = cmds.spaceLocator()[0]
        result = tf.setWSRot(loc)((4,2,1))
        self.assertEquals(result, None)

