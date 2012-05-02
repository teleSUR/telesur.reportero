# -*- coding: utf-8 -*-

import unittest2 as unittest

from telesur.reportero.config import PROJECTNAME
from telesur.reportero.testing import INTEGRATION_TESTING


class InstallTest(unittest.TestCase):
    """Ensure the NITF package is properly installed.
    """

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_installed(self):
        qi = getattr(self.portal, 'portal_quickinstaller')
        self.assertTrue(qi.isProductInstalled(PROJECTNAME))

    def test_permissions_roles(self):
        permission = 'telesur.reportero: Can add an Anonymous Report'
        roles = self.portal.rolesOfPermission(permission)
        roles = [r['name'] for r in roles if r['selected']]
        self.assertEqual(roles, ['Anonymous'])


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
