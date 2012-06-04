function orderReport() {
  var items = $(".report-item");
  var size = items.length;
  if(size) {
    var i = 0;
    var j = 1;
    height = 0;
    for(i=0; i<size ;i++) {
      item = $(items[i])
      item.css("position","absolute");
      item.css("left", height + "px")
      if(i%2==1) {
          item.css("top", "130px")
          height = 180 * j;
      j++;
      } else {
          item.css("top", "0px");
      }
    }
  }
}


$(document).ready(function() {
    $('a.edit-report').prepOverlay({
         subtype: 'ajax',
         filter: '#content>*',
         formselector: 'form',
         noform: 'reload'
        });

//     $('a.view-report').prepOverlay({
//          subtype: 'ajax',
//          filter: '#content>*',
//          formselector: 'form',
//          noform: 'reload'
//         });

});