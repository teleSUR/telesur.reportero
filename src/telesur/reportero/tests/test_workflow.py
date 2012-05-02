# -*- coding: utf-8 -*-

import unittest2 as unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import setRoles
from plone.app.testing import login
from plone.app.testing import logout

from telesur.reportero.testing import INTEGRATION_TESTING


class WorkflowTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def _loginAsManager(self):
        login(self.portal, TEST_USER_NAME)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def setUp(self):
        self.portal = self.layer['portal']
        self.wt = getattr(self.portal, 'portal_workflow')
        self.portal_membership = getattr(self.portal, 'portal_membership')
        self.checkPermission = self.portal_membership.checkPermission
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('telesur.reportero.ireport', 'test-i-report')
        self.folder = self.portal['test-i-report']
        self.folder.invokeFactory('telesur.reportero.anonreport', 'r1')
        self.report = self.folder['r1']

    def test_workflows_installed(self):
        ids = self.wt.getWorkflowIds()
        self.assertTrue('anonreport_workflow' in ids)
        self.assertTrue('ireport_workflow' in ids)

    def test_default_workflow(self):
        chain = self.wt.getChainForPortalType('telesur.reportero.ireport')
        self.assertEqual(len(chain), 1)
        self.assertEqual(chain[0], 'ireport_workflow')

        chain = self.wt.getChainForPortalType('telesur.reportero.anonreport')
        self.assertEqual(len(chain), 1)
        self.assertEqual(chain[0], 'anonreport_workflow')

    def test_workflow_initial_state(self):
        review_state = self.wt.getInfoFor(self.folder, 'review_state')
        self.assertEqual(review_state, 'private')

        review_state = self.wt.getInfoFor(self.report, 'review_state')
        self.assertEqual(review_state, 'private')

    def test_anonymous_can_add_reports(self):

        logout()
        self.folder.invokeFactory('telesur.reportero.anonreport',
                                  'test-anon-report')
        self.assertTrue('test-anon-report' in self.folder)

    def test_question_not_visible_by_anonymous_if_it_is_not_published(self):
        checkPermission = self.checkPermission
        logout()
        self.folder.invokeFactory('telesur.reportero.anonreport',
                                  'test-anon-report')
        self.assertTrue('test-anon-report' in self.folder)

        report = self.folder['test-anon-report']

        # Esto es correcto, podemos agregar como anonimo, pero no podemos verlo
        self.assertNotEqual(checkPermission('View', report), 1)

        self._loginAsManager()

        self.wt.doActionFor(report, 'set_revised')

        logout()
        self.assertNotEqual(checkPermission('View', report), 1)
        self._loginAsManager()

        self.wt.doActionFor(report, 'set_edited')

        logout()
        self.assertNotEqual(checkPermission('View', report), 1)
        self._loginAsManager()

        self.wt.doActionFor(report, 'set_organized')

        logout()
        self.assertNotEqual(checkPermission('View', report), 1)
        self._loginAsManager()

        self.wt.doActionFor(report, 'publish')

        logout()

        self.assertEqual(checkPermission('View', report), 1)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
