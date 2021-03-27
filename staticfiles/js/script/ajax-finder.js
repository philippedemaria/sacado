define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement ajax-finder.js OK");

 

 
        $('#search_question').on('keyup', function (event) {

            console.log("test") ;
 
            let quizz_id = $("#quizz_id").val();
            let keywords = $(this).val();
            if (keywords.length < 4 )
            {
              keywords = "no_finder";
            }

                let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
     
                $("#small_loader").html("<i class='fa fa-spinner fa-pulse fa-2x fa-fw'></i>");
                
     

                $.ajax(
                        {
                        type: "POST",
                        dataType: "json",
                        traditional: true,
                        data: {
                            'keywords': keywords,
                            'quizz_id': quizz_id,
                            csrfmiddlewaretoken: csrf_token
                        },
                        url:"../../ajax_find_question",
                        success: function (data) {
     
                            $('#questions_finder').html("").html(data.html);
                            $("#small_loader").html(""); 
                            
                            }
                        }
                    )



        }); 








    });
});