import unittest
from nose.plugins.attrib import attr

from .. import lazy


class Test_lazy (unittest.TestCase):

    def test_lazy_makesListLazy (self):
        xs = [1,2,3]
        ys = lazy.lazy(xs)
        self.assertEquals(ys.next(), 1)
        self.assertEquals(ys.next(), 2)
        self.assertEquals(ys.next(), 3)
        self.assertRaises(StopIteration, ys.next)

    def test_lazy_isIdempotent (self):
        xs = lazy.lazy(lazy.lazy([1,2]))
        self.assertEquals(xs.next(), 1)
        self.assertEquals(xs.next(), 2)
        self.assertRaises(StopIteration, xs.next)

    def test_strict_hasNoEffectOnGenerator (self):
        self.assertEquals(lazy.strict((x for x in [1,2,3])), [1,2,3])


class Test_strict (unittest.TestCase):

    def test_strict_makesGeneratorStrict (self):
        xs = (x for x in [1,2,3])
        self.assertEquals(xs.next(), 1)
        self.assertEquals(lazy.strict(xs), [2,3])

    def test_strict_isIdempotent (self):
        self.assertEquals(lazy.strict(lazy.strict((x for x in [1,2,3]))), [1,2,3])

    def test_strict_hasNoEffectOnList (self):
        self.assertEquals(lazy.strict([1,2,3]), [1,2,3])

