$(document).ready(function () {
  $(".download-upload-widget").click(function() {
    var value = $(this).attr("file_value");
    $("#download_frame").attr("src", "http://upload.tlsur.net/files/" + value);
  });
  
});