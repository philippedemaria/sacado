define(['jquery',  'bootstrap', ], function ($) {
    $(document).ready(function () {
 
        console.log(" ajax-play-quizz chargé ");

 
        var i = 0;
        setInterval(function(){
            $("body").removeClass("bg1, bg2, bg3, bg4, bg5, bg6, bg7, bg8").addClass("bg"+(i++%8 + 1));
        }, 4000);
 



        var ajaxFn = function () {
                $.ajax({
                    url: "ajax_start_playing_student",
                    success: function (data) {
                        if (data == 'True') {

                            // afichage des question
                            $('#get_the_question_in_the_form').html(data.html);
                            clearTimeout(timeOutId);//stop the timeout

                        } else {
                            timeOutId = setTimeout(ajaxFn, 5000);//set the timeout again
                            console.log("call");//check if this is running
                        }
                    }
                });
        }
         

        timeOutId = setTimeout(ajaxFn, 500);




 

 

 


 




    });
});