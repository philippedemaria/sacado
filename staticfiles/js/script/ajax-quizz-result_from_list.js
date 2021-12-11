define(['jquery',  'bootstrap' ], function ($) {
    $(document).ready(function () {
 
 
    console.log(" ajax-quizz-result_from_list chargé ");
 
 

        $('.show_my_quizz_result').on('click', function (event) {

            let quizz = $(this).data("quizz");
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
 
            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    traditional: true,
                    data: {
                        'quizz': quizz,                      
                        csrfmiddlewaretoken: csrf_token
                    },
                    url : "../../../tool/ajax_show_my_result",
                    success: function (data) {
 
                        $("#my_result").html(data.html); 
                    }
                }
            )
        });


        



 
    });
});