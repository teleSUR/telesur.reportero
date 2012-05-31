import zope.component
import zope.interface
import zope.schema.interfaces

from z3c.form import interfaces
from z3c.form.widget import FieldWidget
from z3c.form.browser.text import TextWidget
from plone.registry.interfaces import IRegistry

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from telesur.reportero import _
from telesur.reportero.controlpanel import IReporteroSettings


def get_url():
    registry = zope.component.getUtility(IRegistry)
    settings = registry.forInterface(IReporteroSettings)
    return settings.upload_url

class UploadWidget(TextWidget):
    """Input type upload widget implementation."""
    input_template = ViewPageTemplateFile('upload_input.pt')
    display_template = ViewPageTemplateFile('upload_display.pt')
    
    klass = u'upload-widget'
    
    
    # JavaScript template
    js_template_input = """\
    (function($) {
        function endsWith(str, suffix) {
            return str.indexOf(suffix, str.length - suffix.length) !== -1;
        }
        
        $().ready(function() {
        $("#formfield-form-widgets-file_type").css("display", "none");
        $('#%(id)s').css('display','none');
         var uploader = new qq.FileUploader({
             element: $('#%(id_uploader)s')[0],
             action: '%(upload_url)s',
             debug: true,
             onComplete: function(id, filename, result) {
               if (result['status'] === "success") {
                 regex = "^[a-zA-Z0-9]+\.[a-zA-Z]{3}$";
                 var file_id = result['id'];
                 $('#%(id)s').val(file_id);
                 $('#%(id_uploader)s').css("display", "none");
                 if(endsWith(filename,"jpg") || endsWith(filename,"gif") ||
                 endsWith(filename,"png") || endsWith(filename,"jpeg") ||
                 endsWith(filename,"JPG") || endsWith(filename,"GIF") ||
                  endsWith(filename,"PNG") || endsWith(filename,"JPEG")) {
                    $("#form-widgets-file_type").val("image");
                 } else { $("#form-widgets-file_type").val("video");}
               } else {
                $("#formfield-%(id)s .fieldErrorBox").text("%(upload_error)s");
               }
             }
         });

        });
    })(jQuery);
    """

    js_template_display = """\
    (function($) {
        $().ready(function() {
         $(".download-upload-widget").click(function() {
           var value = $(this).attr("file_value");
           $("#download_frame").attr("src", "%(upload_url)s" + value);
         });
        });
    })(jQuery);
    """

    def js_input(self):
        upload_error = _(u"Error uploading file, please try again or use a diferent file")
        return self.js_template_input % dict(id=self.id, 
            id_uploader=self.uploader_id(), upload_url=get_url(),
            upload_error=upload_error)
    
    def js_display(self):
        return self.js_template_display % dict(upload_url=get_url())
    
    def uploader_id(self):
        return self.id + "-uploader"
    
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
    
