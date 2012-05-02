# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.component import createObject
from zope.component import queryUtility

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from plone.dexterity.interfaces import IDexterityFTI

from telesur.reportero.content.anonreport import IAnonReport
from telesur.reportero.testing import INTEGRATION_TESTING


class IntegrationTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        # Reports are only addable inside i-report sections
        self.portal.invokeFactory('telesur.reportero.ireport', 's1')
        self.section = self.portal['s1']
        workflow_tool = getattr(self.portal, 'portal_workflow')
        workflow_tool.doActionFor(self.section, 'publish')

    def test_addable_inside_i_report_section(self):
        self.section.invokeFactory('telesur.reportero.anonreport', 'r1')
        r1 = self.section['r1']
        self.assertTrue(IAnonReport.providedBy(r1))

    def test_not_globally_addable(self):
        fti = queryUtility(IDexterityFTI, name='telesur.reportero.anonreport')
        self.assertFalse(fti.global_allow)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='telesur.reportero.anonreport')
        self.assertNotEquals(None, fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='telesur.reportero.anonreport')
        schema = fti.lookupSchema()
        self.assertEquals(IAnonReport, schema)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='telesur.reportero.anonreport')
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(IAnonReport.providedBy(new_object))

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
