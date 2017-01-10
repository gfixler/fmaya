import unittest
from nose.plugins.attrib import attr

from .. import name


class Test_withNS (unittest.TestCase):

    def test_withNS_prependsColonWhenNSIsEmptyString (self):
        self.assertEquals(name.withNS("")("foo"), ":foo")

    def test_withNS_joinsAroundColon (self):
        self.assertEquals(name.withNS("bar")("foo"), "bar:foo")


class Test_stripNS (unittest.TestCase):

    def test_stripNS_preservesStringWithNoNamespaces (self):
        self.assertEquals(name.stripNS("nsfree"), "nsfree")

    def test_stripNS_removesOneNamespace (self):
        self.assertEquals(name.stripNS("foo:tball"), "tball")

    def test_stripNS_removesTwoNamespaces (self):
        self.assertEquals(name.stripNS("bar:foo:tball"), "tball")

    def test_stripNS_removesManyNamespaces (self):
        self.assertEquals(name.stripNS("a:b:c:d:e"), "e")

