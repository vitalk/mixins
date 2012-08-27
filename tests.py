#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest
import doctest

from mixins import UserMixin


class User(UserMixin):
    pass


class TestMixins(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_usermixin(self):
        """Test user mixin."""
        user = User(name='vital')
        self.assertEqual(user.name, 'vital')
        self.assertRaises(AssertionError, user.verify_password, 'secret')
        user.password = 'secret'
        self.assertEqual(user.verify_password('secret'), True)
        self.assertEqual(user.verify_password('oops'), False)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestMixins))
    suite.addTest(doctest.DocFileSuite('mixins.py', globs=globals()))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
