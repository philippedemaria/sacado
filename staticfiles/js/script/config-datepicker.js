
define(['jquery','bootstrap', 'ui','datepicker','datetimepicker'], function ($) {
    //Date picker
    $('.datepicker').datepicker({
        format: "yyyy-mm-dd",
        language: "fr",
        todayHighlight: true
    });



      $('.datetimepicker').datetimepicker({

		        language: "fr",
		        todayHighlight: true,
                format: "yyyy-mm-dd hh:ii"

             });
    




});

   