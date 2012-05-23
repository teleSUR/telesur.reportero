from z3c.form.browser.text import TextWidget
import zope.component
import zope.interface
import zope.schema.interfaces

from z3c.form import interfaces
from z3c.form.widget import FieldWidget

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class UploadWidget(TextWidget):
    """Input type upload widget implementation."""
    input_template = ViewPageTemplateFile('upload_input.pt')
    display_template = ViewPageTemplateFile('upload_display.pt')
    
    klass = u'upload-widget'
    
    def render(self):
        if self.mode == interfaces.DISPLAY_MODE:
            return self.display_template(self)
        else:
            return self.input_template(self)
    

@zope.component.adapter(zope.schema.interfaces.IField, interfaces.IFormLayer)
@zope.interface.implementer(interfaces.IFieldWidget)
def UploadFieldWidget(field, request):
    """IFieldWidget factory for UploadWidget."""
    return FieldWidget(field, UploadWidget(request))