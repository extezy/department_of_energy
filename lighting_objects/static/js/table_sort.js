
//function search(ele) {
//    if(event.keyCode == 13) {
//        var select = $('#select_for_search').val()
////        if(select != "0"){
////            location.href = "/?" + select + "=" + ele.value;
////        }
//        location.href = "?q=" + ele.value;
//    }
//}

//
//$(document).ready(function() {
//
////    $('#table_sort').DataTable();
//  $('#table_sort').dataTable({
//
//    initComplete: function () {
//      this.api().columns().every( function () {
//          var column = this;
//          var select = $('<select  class="browser-default custom-select form-control-sm"><option value="" selected>Search</option></select>')
//              .appendTo( $(column.footer()).empty() )
//              .on( 'change', function () {
//                  var val = $.fn.dataTable.util.escapeRegex(
//                      $(this).val()
//                  );
//
//                  column
//                      .search( val ? '^'+val+'$' : '', true, false )
//                      .draw();
//              });
//
//          column.data().unique().sort().each( function ( d, j ) {
//              select.append( '<option value="'+d+'">'+d+'</option>' )
//          });
//      } );
//  }
//  });
//});

$(document).ready(function() {
    $('#table_sort').dataTable();
});