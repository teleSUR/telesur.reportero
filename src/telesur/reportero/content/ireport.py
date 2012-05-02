# -*- coding: utf-8 -*-
from five import grok

from plone.directives import dexterity, form

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CMFCore.utils import getToolByName

from zope.security import checkPermission

class IIReport(form.Schema):
    """
    A section that contains reports
    """

class View(dexterity.DisplayForm):
    grok.context(IIReport)
    grok.require('zope2.View')

    def render(self):
        pt = ViewPageTemplateFile('ireport_templates/ireport_view.pt')
        return pt(self)

    def can_add_reports(self):
        return checkPermission('telesur.reportero.anonreportAddable', self.context)

    def can_edit(self):
        return checkPermission('cmf.ModifyPortalContent', self.context)

    def _get_catalog_results(self, state):
        pc = getToolByName(self.context, 'portal_catalog')

        ct = "telesur.reportero.anonreport"
        path='/'.join(self.context.getPhysicalPath())
        sort_on='Date'
        sort_order='reverse'

        results = pc.unrestrictedSearchResults(portal_type=ct,
                                               review_state=state,
                                               sort_on=sort_on,
                                               sort_order=sort_order,
                                               path=path)

        return results

    def get_published_reports(self):
        reports = self._get_catalog_results('published')
        return reports

    def get_non_published_reports(self):
        reports = self._get_catalog_results('private')
        reports += self._get_catalog_results('revised')
        reports += self._get_catalog_results('rejected')
        reports += self._get_catalog_results('edited')
        reports += self._get_catalog_results('organized')
        return reports
