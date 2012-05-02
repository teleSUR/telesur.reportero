# -*- coding: utf-8 -*-

import unittest2 as unittest
import doctest

from plone.testing import layered

from telesur.reportero.testing import FUNCTIONAL_TESTING


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(doctest.DocFileSuite('tests/functional.txt',
                                     package='telesur.reportero'),
                layer=FUNCTIONAL_TESTING),
        ])
    return suite
