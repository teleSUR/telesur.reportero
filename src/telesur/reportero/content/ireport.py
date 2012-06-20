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

BATCH_SIZE = 5
class View(dexterity.DisplayForm):
    grok.context(IIReport)
    grok.require('zope2.View')
    
    def update(self):
        self.actual = 0
        self.total = 0
        publics = self.get_published_reports()
        self.total = len(publics)/BATCH_SIZE
        if 'action' in self.request.keys():
            action = self.request['action']
            if action == 'next':
                self.actual = int(self.request['actual'])
                if len(publics[(self.actual+1)*BATCH_SIZE: (self.actual+2)*BATCH_SIZE]) > 0:
                    self.actual += 1
            elif action == 'prev':
                self.actual = int(self.request['actual'])
                if self.actual > 0:
                    self.actual -= 1
        
        self.publics = publics[self.actual*BATCH_SIZE:(self.actual+1)*BATCH_SIZE]
        self.main_report_new = None
        if self.publics:
            self.main_report_new = self.publics[0]
        
    def render(self):
        pt = ViewPageTemplateFile('ireport_templates/ireport_view.pt')
        return pt(self)

    def can_add_reports(self):
        return checkPermission('telesur.reportero.anonreportAddable',
                               self.context)

    def can_edit(self):
        return checkPermission('cmf.ModifyPortalContent', self.context)

    def _get_catalog_results(self, state=None):
        pc = getToolByName(self.context, 'portal_catalog')

        ct = "telesur.reportero.anonreport"
        path='/'.join(self.context.getPhysicalPath())
        sort_on='Date'
        sort_order='reverse'
        if state:
            results = pc.unrestrictedSearchResults(portal_type=ct,
                                               review_state=state,
                                               sort_on=sort_on,
                                               sort_order=sort_order,
                                               path=path)
        else:
            results = pc.unrestrictedSearchResults(portal_type=ct,
                                               sort_on=sort_on,
                                               sort_order=sort_order,
                                               path=path)
            

        return results

    def get_all_reports(self):
        reports = self._get_catalog_results()
        return reports
        
    def get_published_reports(self):
        reports = self._get_catalog_results('published')
        return reports

    def get_non_published_reports(self):
        pc = getToolByName(self.context, 'portal_catalog')
        ct = "telesur.reportero.anonreport"
        path='/'.join(self.context.getPhysicalPath())
        sort_on='Date'
        sort_order='reverse'
        states = ['private','revised', 'rejected', 'edited',  'organized']
        filters = {'review_state':{'operator': 'or', 'query': states},
                    'portal_type': ct, 'path':path, 'sort_on':sort_on,
                    'sort_order':sort_order}
        reports = pc.searchResults(filters)
        return reports


BACH_SIZE = 20
class ListadoReportView(View):
    grok.require('cmf.ModifyPortalContent')
    grok.name('listado-report')
    
    def update(self):
        self.actual = 0
        self.total = 0
        publics = self.get_non_published_reports()
        self.total = len(publics)/BACH_SIZE
        if 'action' in self.request.keys():
            action = self.request['action']
            if action == 'next':
                self.actual = int(self.request['actual'])
                if len(publics[(self.actual+1)*BACH_SIZE: (self.actual+2)*BACH_SIZE]) > 0:
                    self.actual += 1
            elif action == 'prev':
                self.actual = int(self.request['actual'])
                if self.actual > 0:
                    self.actual -= 1
        self.publics = publics[self.actual*BACH_SIZE:(self.actual+1)*BACH_SIZE]
    
    def render(self):
        pt = ViewPageTemplateFile('ireport_templates/listadoreport_view.pt')
        return pt(self)
