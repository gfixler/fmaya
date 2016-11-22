import unittest
from nose.plugins.attrib import attr

from .. import scene


class Test_toValidMayaName (unittest.TestCase):

    def test_toValidMayaName_keepsValidName (self):
        self.assertEquals(scene.toValidMayaName("a_valid_name"), "a_valid_name")

    def test_toValidMayaName_keepsAnotherValidName (self):
        self.assertEquals(scene.toValidMayaName("ThisIsFine_too"), "ThisIsFine_too")

    def test_toValidMayaName_replacesDots (self):
        self.assertEquals(scene.toValidMayaName(".foo.bar.baz."), "_foo_bar_baz_")

    def test_toValidMayaName_replacesSpaces (self):
        self.assertEquals(scene.toValidMayaName(" foo bar baz "), "_foo_bar_baz_")

    def test_toValidMayaName_replacesPunctuation (self):
        self.assertEquals(scene.toValidMayaName("&foo*bar#baz%"), "_foo_bar_baz_")

    def test_toValidMayaName_replacesManyThings (self):
        self.assertEquals(scene.toValidMayaName("  This 'is' a test!"), "__This__is__a_test_")

