define(['jquery', 'bootstrap', 'ui', 'ui_sortable'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-dashboard_admin.js OK");
 
 


        setTimeout(function(){ 
           $(".messages").css('display', "none"); 
        }, 5000);






        $('.show_help1').on('click', function (event) {
            $("#show_div_help1").toggle(300) ;
        });

        $('.show_help2').on('click', function (event) {
            $("#show_div_help2").toggle(300) ;
        });

        $('.show_help3').on('click', function (event) {
            $("#show_div_help3").toggle(300) ;
        });


        $('.show_help4').on('click', function (event) {
            $("#show_div_help4").toggle(300) ;
        });

        $('.show_help5').on('click', function (event) {
            $("#show_div_help5").toggle(300) ;
        });

    });        
});