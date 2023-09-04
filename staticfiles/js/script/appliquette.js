$(document).ready(function () {
 
 
        console.log("---- NEW test ajax-appliquette.js ---") ;  



        var screen_size = $(window).width()  ;


        var width = 2*parseInt($('#appliquette').find("iframe").attr("width"));
        var height = 2*parseInt($('#appliquette').find("iframe").attr("height")); 
        var coeff = width/height   ;                                 

        // if (width < screen_size){
        //     $('#projection_div').find("iframe").attr("width", width); 
        //     $('#projection_div').find("iframe").attr("height", height);
        // }
        // else{
            new_size = 0.8*screen_size ; 
            $('#appliquette').find("iframe").attr("width", new_size ); 
            $('#appliquette').find("iframe").attr("height", new_size / coeff );
        //}

  
 

});

 
