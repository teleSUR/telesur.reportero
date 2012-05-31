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
            default=u"http://upload.tlsur.net/files/",
            required=True)
    
    multimedia_url = schema.TextLine(
            title=_(u'Upload url'),
            default=u"http://multimedia.tlsur.net/api",
            required=True)
    
    security_key = schema.TextLine(
            title=_(u'Upload key'),
            default=u'k4}"-^30C$:3l04$(/<5"7*6|Ie"6x',
            required=True)
    
    key = schema.TextLine(
            title=_(u'Upload key'),
            default=u'telesursoyreporteroplonepruebas',
            required=True)

class ReporteroettingsEditForm(controlpanel.RegistryEditForm):
    schema = IReporteroSettings
    label = _(u'Soy Reportero Settings')
    description = _(u'Here you can modify the settings for telesur.reportero.')



class ReporteroSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = ReporteroettingsEditForm
