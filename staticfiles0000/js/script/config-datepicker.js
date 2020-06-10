
define(['jquery','bootstrap', 'ui','datepicker'], function ($) {
    //Date picker
    $('.datepicker').datepicker({
        format: "yyyy-mm-dd",
        language: "fr",
        todayHighlight: true
    });
});

  