# -*- coding: utf-8 -*-

from five import grok

from plone.dexterity.content import Item

from plone.directives import dexterity, form

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.namedfile.field import NamedBlobFile

from telesur.reportero import _

from z3c.form.interfaces import IEditForm

from zope import schema

from zope.interface import implements

from zope.app.container.interfaces import IObjectAddedEvent


class IAnonReport(form.Schema):
    """
    A report that any site visitor can add.
    """

    status = schema.Bool(
            title=_(u'Status'),
            description=_(u'help_status',
                          default=u'Select status.'),
        )

    original_file = NamedBlobFile(
            title=_(u'File'),
            description=_(u'help_original_file',
                          default=u'Load here your image or video file.'),
            required=True,
        )

    date = schema.Datetime(
            title=_(u'Date'),
            description=_(u'help_date',
                          default=(u'Enter here the date in which this photo '
                                    'or video was taken.')),
            required=True,
        )

    form.omitted('edited_file')
    form.no_omit(IEditForm, 'edited_file')
    edited_file = NamedBlobFile(
            title=_(u'Edited File'),
            description=_(u'help_edited_file',
                          default=(u'You can load here a modified '
                                    'version of the original file.')),
            required=False,
        )


class AnonReport(Item):
    """

    """
    implements(IAnonReport)


@grok.subscribe(IAnonReport, IObjectAddedEvent)
def redirect_after_add(obj, event):
    """
    se redirige al padre en lugar de permanecer en el reporte recien
    cargado.
    """
    parent = obj.aq_inner.aq_parent
    obj.REQUEST.RESPONSE.redirect(parent.absolute_url())

class View(dexterity.DisplayForm):
    grok.context(IAnonReport)
    grok.require('zope2.View')

    def render(self):
        pt = ViewPageTemplateFile('ianonreport_templates/ianonreport_view.pt')
        return pt(self)