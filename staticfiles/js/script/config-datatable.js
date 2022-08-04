
define(['jquery', 'datatables','datatables_bootstrap'], function ($) {



$('.standard_tab_10').dataTable( {
    "pageLength": 10,
    "ordering": true,
    "info":     true
} );



$('.standard_tab_1000').dataTable( {
    "pageLength": 1000,
    "ordering": false,
    "info":     false
} );


$('.ordering_tab_1000').dataTable( {
    "pageLength": 1000,
    "info":     false
} );


$('#standard_tab').dataTable( {
    "order": [],
    "pageLength": 50,
    "ordering": false,
    "info":     false
} );

$('.standard_tab_sort').dataTable( {
    "order": [],
    "pageLength": 50,
    "info":     false
} );

 

$('.display_info').dataTable( {
    "order": [],
    "pageLength": 50,
} );
 
 $('table.display').DataTable({
		"pageLength": 50,
		"ordering": false,
        "info":     false
				} );

 $('table.display100').DataTable({
		"pageLength": 100,
		"ordering": false,
        "info":     false
				} );
 
 
$('.standard_tab_sort300').dataTable( {
    "pageLength": 300,
    "info":     false
} );

$('.standard_tab_sort300_no_paiement').dataTable( {
    "order": [],
    "pageLength": 300,
    "info":     false
} );




 
$('.standard_tab_sort2000').dataTable( {
    "order": [],
    "pageLength": 2000,
    "info":     false 
} );


$('table.display1000').DataTable({
                "pageLength": 1000,
                "ordering": false,
                "retrieve": true,
                "paging": false,
                "info":  false
                });


 $('table.display_no_details20').DataTable({
		"pageLength": 20,
		"ordering": false,
		"paging": false,
        "info":     false				
    } );

 $('table.display_no_details50').DataTable({
        "pageLength": 50,
        "paging"    : false,
        "info"      :     false               
    } );


 $('table.display_no_details100').DataTable({
        "pageLength": 100,
        "paging"    : false,
        "info"      : false               
    } );





});