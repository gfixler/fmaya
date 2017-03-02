import unittest
from nose.plugins.attrib import attr

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

