define(['jquery',  'bootstrap' ], function ($) {
    $(document).ready(function () {
 
 
    console.log(" ajax-quizz-complement-is_numeric chargé ");
 

 

        $('#id_is_numeric').on('change', function (event) {
            $('.div_is_mark').toggle(300) ; 
        });
        $('#id_is_video').on('change', function (event) {
            $('.div_is_ranking').toggle(300) ;
            $('.div_interslide').toggle(300) ; 
        });
        $('#id_is_publish').on('change', function (event) {
            $('.div_time').toggle(300) ; 
        });
 
 


        


 
    });
});