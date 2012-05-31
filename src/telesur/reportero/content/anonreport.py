# -*- coding: utf-8 -*-
import httplib2
import hashlib
from urllib import urlencode

from zope import schema
import zope.component
from zope.interface import implements
from zope.app.container.interfaces import IObjectAddedEvent
from zope.security import checkPermission
from zope.interface import Invalid
from zope.event import notify

from z3c.form import button
from z3c.form.interfaces import ActionExecutionError

from five import grok

from z3c.form.interfaces import IEditForm, IDisplayForm

from plone.dexterity.content import Item
from plone.dexterity.events import EditFinishedEvent
from plone.directives import dexterity, form
from plone.namedfile.field import NamedBlobFile
from plone.registry.interfaces import IRegistry

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage

from telesur.reportero import _
from telesur.reportero.widgets.upload_widget import UploadFieldWidget
from telesur.reportero.controlpanel import IReporteroSettings


class IAnonReport(form.Schema):
    """
    A report that any site visitor can add.
    """

    status = schema.Bool(
            title=_(u'Status'),
            description=_(u'help_status',
                          default=u'Select status.'),
        )
    
    form.widget(file_id=UploadFieldWidget)
    form.omitted(IEditForm, 'file_id')
    file_id = schema.Text(
            title=_(u'File'),
             description=_(u'upload video or image'),
             required=True,
    )
    
    form.omitted('file_slug')
    file_slug = schema.Text(required=False)

    date = schema.Date(
            title=_(u'Date'),
            description=_(u'help_date',
                          default=(u'Enter here the date in which this photo '
                                    'or video was taken.')),
            required=True,
        )

    form.omitted('edited_file_id')
    form.no_omit(IEditForm, 'edited_file_id')
    form.widget(edited_file_id=UploadFieldWidget)
    edited_file_id = schema.Text(
            title=_(u'Edited File'),
             description=_(u'upload edited video or image'),
             required=False,
    )
    
    form.omitted('edited_file_slug')
    edited_file_slug = schema.Text(required=False)
    
    form.omitted(IDisplayForm, 'file_type')
    file_type = schema.TextLine(
             required=False
    )

class AnonReport(Item):
    """

    """
    implements(IAnonReport)
    
    def is_published_resource(self):
        slug = self.file_slug
        if self.edited_file_slug:
            slug = self.edited_file_slug
        body = {}
            

def firma_request(params_dict, key, secret):
    params_dict['key'] = key
    cadena = u'%s' % secret
    for name in sorted(params_dict.iterkeys()):
        cadena += u'%s%s' % (name, params_dict[name])
    return hashlib.md5(cadena).hexdigest()

def get_multimedia_url():
    registry = zope.component.getUtility(IRegistry)
    settings = registry.forInterface(IReporteroSettings)
    return settings.multimedia_url

def get_security_key():
    registry = zope.component.getUtility(IRegistry)
    settings = registry.forInterface(IReporteroSettings)
    return settings.security_key

def get_key():
    registry = zope.component.getUtility(IRegistry)
    settings = registry.forInterface(IReporteroSettings)
    return settings.key

class Edit(dexterity.EditForm):
    """ Default edit for Ideas
    """
    grok.context(IAnonReport)

    @button.buttonAndHandler(_(u'Save'))
    def handleSaveAndSend(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        if 'edited_file_id' in data.keys() and self.context.edited_file_id != data['edited_file_id']:
            body = {}
            if 'file_type' in data.keys():
                file_type = data['file_type']
            else:
                raise ActionExecutionError(Invalid(_(u"Error creating the report, please try again")))
            if 'IBasic.title' in data.keys():
                body['titulo'] = data['IBasic.title']
            if 'IBasic.description' in data.keys():
                body['descripcion'] = data['IBasic.description']
            body['archivo'] = data['edited_file_id']
            body['tipo'] = 'soy-reportero'

            if file_type == "image":
                url = get_multimedia_url + '/imagen/'
            else:
                url = get_multimedia_url + '/clip/'
            headers = {'Accept': 'application/json'}
            key = get_security_key()
            sign_key = firma_request(body, get_key(), key)
            body['signature'] = sign_key
            http = httplib2.Http()
            response, content = http.request(url, 'POST', headers=headers, body=urlencode(body))
            if 'status' not in response.keys() or response['status'] != '200':
                raise ActionExecutionError(Invalid(_(u"Error creating the report, please try again")))
            
        self.applyChanges(data)
        IStatusMessage(self.request).addStatusMessage(_(u"Changes saved"), "info")
        self.request.response.redirect(self.nextURL())
        notify(EditFinishedEvent(self.context))


class Add(dexterity.AddForm):
    """ Default edit for Ideas
    """
    grok.name('telesur.reportero.anonreport')
    grok.context(IAnonReport)

    @button.buttonAndHandler(_('Save'), name='save')
    def handleAdd(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        body = {}
        if 'file_type' in data.keys():
            file_type = data['file_type']
        else:
            raise ActionExecutionError(Invalid(_(u"Error creating the report, please try again")))
        if 'IBasic.title' in data.keys():
            body['titulo'] = data['IBasic.title']
        if 'IBasic.description' in data.keys():
            body['descripcion'] = data['IBasic.description']
        if 'file_id' in data.keys():
            body['archivo'] = data['file_id']
        body['tipo'] = 'soy-reportero'
        
        if file_type == "image":
            url = get_multimedia_url + '/imagen/'
        else:
            url = get_multimedia_url + '/clip/'
        headers = {'Accept': 'application/json'}
        key = get_security_key()
        sign_key = firma_request(body, get_key(), key)
        body['signature'] = sign_key
        http = httplib2.Http()
        response, content = http.request(url, 'POST', headers=headers, body=urlencode(body))
        if 'status' not in response.keys() or response['status'] != '200':
            raise ActionExecutionError(Invalid(_(u"Error creating the report, please try again")))
        obj = self.createAndAdd(data)
        if obj is not None:
            # mark only as finished if we get the new object
            self._finishedAdd = True
            IStatusMessage(self.request).addStatusMessage(_(u"Item created"), "info")

        return obj

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
    
    def can_edit(self):
        permission = 'cmf.ModifyPortalContent'
        return checkPermission(permission, self.context)

    def render(self):
        pt = ViewPageTemplateFile('ianonreport_templates/ianonreport_view.pt')
        return pt(self)