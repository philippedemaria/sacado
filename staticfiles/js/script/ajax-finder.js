define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {


        console.log("chargement ajax-finder.js OK");

 
        $('#search_question_waiting').on('change', function (event) {

            let quizz_id = $("#quizz_id").val();
            let waiting_id = $("#search_question_waiting").val();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
     
            $("#small_loader").html("<i class='fa fa-spinner fa-pulse fa-3x fa-fw'></i>");
                
     

                $.ajax(
                        {
                        type: "POST",
                        dataType: "json",
                        traditional: true,
                        data: {
                            'waiting_id': waiting_id,
                            'quizz_id': quizz_id,
                            csrfmiddlewaretoken: csrf_token
                        },
                        url:"../../ajax_find_question_waiting",
                        success: function (data) {
     
                            $('#questions_finder').html("").html(data.html);
                            $("#small_loader").html(""); 
                            
                            }
                        }
                    )



        }); 






 
        $('#search_question').on('keyup', function (event) {
 
            let quizz_id = $("#quizz_id").val();
            let keywords = $(this).val();
            if (keywords.length > 3 )
            {
             


                let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
     
                $("#small_loader").html("<i class='fa fa-spinner fa-pulse fa-3x fa-fw'></i>");
                
     

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
            }


        }); 








    });
});