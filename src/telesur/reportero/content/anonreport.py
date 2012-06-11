# -*- coding: utf-8 -*-
from zope import schema
from zope.interface import implements
from zope.app.container.interfaces import IObjectAddedEvent
from zope.security import checkPermission
from zope.interface import Invalid
from zope.event import notify
from zope.component import getUtility

from z3c.form import button
from z3c.form.interfaces import ActionExecutionError

from five import grok

from z3c.form.interfaces import IEditForm, IDisplayForm

from plone.app.dexterity.behaviors.exclfromnav import IExcludeFromNavigation
from plone.dexterity.content import Item
from plone.dexterity.events import EditFinishedEvent
from plone.directives import dexterity, form
from plone.namedfile.field import NamedBlobFile

from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage

from collective.prettydate.interfaces import IPrettyDate

from telesur.reportero import _
from telesur.reportero.widgets.upload_widget import UploadFieldWidget
from telesur.reportero.multimedia_connect import MultimediaConnect



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

    date = schema.Datetime(
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
    
    def is_image(self):
        return self.file_type == 'image'
    
    def get_slug(self):
        if self.edited_file_slug:
            return self.edited_file_slug
        else:
            return self.file_slug

    def get_file_url(self):
        multimedia_connect = MultimediaConnect()
        response, content = multimedia_connect.get_structure(
            self.get_slug(), self.file_type)
        if response['status'] == '200' and content:
            if not self.is_image() and 'archivo_url' in content:
                return content['archivo_url']     
            else:
                return content['thumbnail_grande']
        return None
    
    def get_thumb_image(self):
        multimedia_connect = MultimediaConnect()
        response, content = multimedia_connect.get_structure(
            self.get_slug(), self.file_type)
        if response['status'] == '200' and 'thumbnail_pequeno' in content:
            return content['thumbnail_pequeno']
        return None
    
    def get_status(self):
        workflowTool = getToolByName(self, "portal_workflow")
        chain = workflowTool.getChainForPortalType(self.portal_type)
        status = workflowTool.getStatusOf(chain[0], self)
        state = status["review_state"]
        return state
    
    def get_date(self):
        date_utility = getUtility(IPrettyDate)
        return date_utility.date(self.date)

# @form.default_value(field = IExcludeFromNavigation['exclude_from_nav'])
# def excludeFromNavDefaultValue(data):
#     return data.request.URL.endswith('++add++telesur.reportero.anonreport')

class Edit(dexterity.EditForm):
    """ Default edit for Ideas
    """
    grok.context(IAnonReport)

    @button.buttonAndHandler(_(u'Save'))
    def handleSaveAndSend(self, action):
        slug = None
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        if 'edited_file_id' in data.keys() and \
            self.context.edited_file_id != data['edited_file_id']:
            body = {}
            if 'file_type' in data.keys():
                file_type = data['file_type']
            else:
                raise ActionExecutionError(Invalid(
                    _(u"Error creating the report, please try again")))
            if 'IBasic.title' in data.keys():
                body['titulo'] = data['IBasic.title']
            if 'IBasic.description' in data.keys():
                body['descripcion'] = data['IBasic.description']
            body['archivo'] = data['edited_file_id']
            body['tipo'] = 'soy-reportero'

            multimedia_connect = MultimediaConnect()
            response, content = multimedia_connect.create_structure(body, file_type)
            slug = None
            if "slug" in content:
                slug = content['slug']
            if 'status' not in response.keys() or response['status'] != '200'\
                or not slug:
                raise ActionExecutionError(Invalid(_(u"Error creating the \
                    report, please try again")))
            data['edited_file_slug'] = slug
            if slug:
                self.context.edited_file_slug = slug
                self.context.reindexObject()
        self.applyChanges(data)
        IStatusMessage(self.request).addStatusMessage(_(u"Changes saved"),
            "info")
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
            raise ActionExecutionError(Invalid(
                _(u"Error creating the report,please try again")))
        if 'IBasic.title' in data.keys():
            body['titulo'] = data['IBasic.title'].encode("utf-8", "ignore")
        if 'file_id' in data.keys():
            body['archivo'] = data['file_id']
        body['tipo'] = 'soy-reportero'
        
        multimedia_connect = MultimediaConnect()
        response, content = multimedia_connect.create_structure(body, file_type)

        if 'status' not in response.keys() or response['status'] != '200':
            raise ActionExecutionError(Invalid(_(u"Error creating the report,\
                please try again")))
        slug = None
        if "slug" in content:
            slug = content['slug']
        else:
            raise ActionExecutionError(Invalid(_(u"Error creating the report,\
                please try again")))

        data['file_slug'] = slug
        obj = self.createAndAdd(data)
        if obj is not None:
            # mark only as finished if we get the new object
            obj.file_slug = slug
            obj.reindexObject()
            self._finishedAdd = True
            IStatusMessage(self.request).addStatusMessage(_(u"Item created"),
                "info")

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