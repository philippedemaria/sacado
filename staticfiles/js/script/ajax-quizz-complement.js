define(['jquery',  'bootstrap' ], function ($) {
    $(document).ready(function () {
 
 
    console.log(" ajax-quizz-complement chargé ");
 
  
        $(document).ready(function(){
            (function(){
                var i = 0;
                setInterval(function(){
                    $("body").removeClass("bg1, bg2, bg3, bg4, bg5, bg6, bg7, bg8").addClass("bg"+(i++%8 + 1));
                }, 4000);
            })();
        });

        $('[type=checkbox]').prop('checked', false); 


 

 
    });
});