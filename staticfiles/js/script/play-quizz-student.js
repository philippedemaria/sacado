define(['jquery',  'bootstrap', ], function ($) {
    $(document).ready(function () {
 
        console.log(" ajax-play-quizz chargé ");

 
        var i = 0;
        setInterval(function(){
            $("body").removeClass("bg1, bg2, bg3, bg4, bg5, bg6, bg7, bg8").addClass("bg"+(i++%8 + 1));
        }, 4000);
 
        $("#after_the_question").hide() ;


        var ajaxFn = function () {

            let gquizz_id = $("#gquizz_id").val() ;
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

                $.ajax({
                    type: "POST",
                    dataType: "json",
                    data: {
                        'gquizz_id': gquizz_id,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "ajax_display_question_to_student",
                    success: function (data) {
                        if (data.is_valid == "True") {
                            // afichage des question
                            $('#get_the_question_in_the_form').html(data.html);
                            clearInterval(timeOutId);//stop the timeout
                            console.log(data.timer) ;
                            setTimeout(ajaxFn, data.timer);
                        } else {
                            timeOutId = setTimeout(ajaxFn, 5000);//set the timeout again
                            console.log("call");//check if this is running
                        }
                    }
                });
        }
         

        timeOutId = setInterval(ajaxFn, 2000);


    });
});