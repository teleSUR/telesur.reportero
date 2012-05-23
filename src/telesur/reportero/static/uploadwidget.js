$(document).ready(function () {
  var uploader = new qq.FileUploader({
      element: $('#file-uploader')[0],
      action: 'http://upload.tlsur.net/files/',
      debug: true,
      onComplete: function(id, filename, result) {
        if (result['status'] === "success") {
          var file_id = result['id'];
          $('#form-widgets-file_id').val(file_id);
          $('#file-uploader').css("display", "none");
        }
      }
  });
  
});