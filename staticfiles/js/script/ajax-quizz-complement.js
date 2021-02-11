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






        $('.generated_quizz').on('click', function (event) {

            let gq_id = $(this).data("gq_id");
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    traditional: true,
                    data: {
                        'gq_id': gq_id,                     
                        csrfmiddlewaretoken: csrf_token
                    },
                    url : "../ajax_show_generated",
                    success: function (data) {

                        $("#body_gq").html("").html(data.html);
                    }
                }
            )
        });








 
    });
});