# -*- coding: utf-8 -*-
from zope import schema
from zope.interface import Interface

from plone.app.registry.browser import controlpanel

from telesur.reportero import _


class IReporteroSettings(Interface):
    """ Interface for the control panel form.
    """

    upload_url = schema.TextLine(
            title=_(u'Upload url'),
            default=u"/upload/",
            required=True)
    
    multimedia_url = schema.TextLine(
            title=_(u'Multimedia url'),
            default=u"http://multimedia.tlsur.net/api",
            required=True)
    
    security_key = schema.TextLine(
            title=_(u'Security key'),
            default=u'Tl&MF4s#e-9x6F[m7]42FyO7mt8Ku',
            required=True)
    
    key = schema.TextLine(
            title=_(u'Upload key'),
            default=u'telesursoyreporteroploneweb',
            required=True)

class ReporteroSettingsEditForm(controlpanel.RegistryEditForm):
    schema = IReporteroSettings
    label = _(u'Soy Reportero Settings')
    description = _(u'Here you can modify the settings for telesur.reportero.')

class ReporteroSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = ReporteroSettingsEditForm