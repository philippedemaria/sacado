define(['jquery',  'bootstrap' ], function ($) {
    $(document).ready(function () {
 
     
        console.log(" full_csv chargé ");
         
          
            $(document).ready(function(){
         

                $('#show_without_username').on('change', function (event) {
                    $("#without_username").show(300) ;
                    $("#with_username").hide(300) ;  
                });

                $('#show_with_username').on('change', function (event) {
                    $("#without_username").hide(300) ;
                    $("#with_username").show(300) ; 
                });
         

                $('#help_utf').on('click', function (event) {
                    $("#show_help_utf").toggle(300) ;
                });
         



            });

    });
});