define(['jquery', 'bootstrap', 'multislider' ], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-dashboard_student.js OK");
 

        $('body').css("overflow-x","hidden");
 
            var numItems = $('#mixedSlider .item').length ;
            var numItems_width = numItems * 350 ;
            var window_width = $( window ).width() ;

            if (numItems_width < window_width ) {

                $(".MS-controls").hide();

            }
            else 
            {

                $('#mixedSlider').multislider({
                    duration: 1000,
                    interval: 10000
                });

            }

        });   



        $(document).on('click',".this_is_an_access_link",function(){
 
            $(this).addClass("no_visu_on_load");
            $(this).parent().append("<i class='fa fa-spinner fa-pulse fa-2x'></i> Chargement en cours.");
        });












});