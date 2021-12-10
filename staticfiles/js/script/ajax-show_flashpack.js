define(['jquery',  'bootstrap' ], function ($) {
    $(document).ready(function () {

        console.log(" show_flashpack chargé ");

        var slideBox = $('.slider ul'),
            slideWidth = 1000 ,
            slideQuantity = $('.slider ul').children('li').length,
            currentSlide = 1 ,
            currentQuestion = 1 ;

        slideBox.css('width', slideWidth*slideQuantity);

     
        function transition(currentSlideInput, slideWidthInput){

            var pxValue = -(currentSlideInput -1) * slideWidthInput ; 
            slideBox.animate( { 'left' : pxValue } )
 
        }


        $('body').on('click', '.navigation',   function (event) {

            let value        = $(this).data("value");

            if (value == "start")
            {
                console.log("start");
            }
            else 
            {

                let flashpack_id = $(this).data("flashpack_id");
                let flashcard_id = $(this).data("flashcard_id");
                let value        = $(this).data("value");
                let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
                $.ajax(
                    {
                        type: "POST",
                        dataType: "json",
                        traditional: true,
                        data: {
                            'flashpack_id': flashpack_id,
                            'flashcard_id': flashcard_id,
                            'value'       : value,                      
                            csrfmiddlewaretoken: csrf_token
                        },
                        url : '../ajax_store_score_flashcard',
                    }
                ) 
            }

            if (currentSlide === slideQuantity)
                    { 
                        currentSlide = 1 ;                                        
                    }
            else 
                    { 
                        currentSlide++ ; 
                    }

            transition(currentSlide, slideWidth )  ;
            event.preventDefault();
        });




        $('body').on('click', '.show_answer',   function (event) { 
            let flashcard_id = $(this).data("flashcard_id");
              $("#answer"+flashcard_id).removeClass("no_visu_onload"); 
              $("#answer"+flashcard_id).show(500); 
              $("#offset").remove();    
              $("#buttons"+flashcard_id).removeClass("no_visu_onload");  
              $("#buttons"+flashcard_id).show(500); 
              $("#data_buttons"+flashcard_id).addClass("no_visu_onload");  
 
        });

        $('body').on('click', '.show_helper',   function (event) { 
            let flashcard_id = $(this).data("flashcard_id");   
              $("#helper"+flashcard_id).removeClass("no_visu_onload");  
              $("#helper"+flashcard_id).toggle(500);
        });



 
        $('.display_info').find("span").css("font-size","18px");   
      

        $('body').on('click', '#this_question_textarea_display',   function (event) { 
 
                let flashcard_id = $(this).data("flashcard_id");
                let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
                $.ajax(
                    {
                        type: "POST",
                        dataType: "json",
                        traditional: true,
                        data: {
                            'flashcard_id': flashcard_id,                      
                            csrfmiddlewaretoken: csrf_token
                        },
                        url : '../ajax_preview_flashcard',
                        success: function (data) {
                            $('#q_of_textarea_display').html(data.html);
                            $("#title_textarea_display").html("Visualisation");
                        }
                    }
                ) 

        });


        $('body').on('click', '.this_comment_display',   function (event) { 
            let flashcard_id = $(this).data("flashcard_id");  
              $("#id_flashcard").val(flashcard_id); 
        });





        $('body').on('click', '.this_show_comments',   function (event) { 
 
                let flashcard_id = $(this).data("flashcard_id");
                let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
                $.ajax(
                    {
                        type: "POST",
                        dataType: "json",
                        traditional: true,
                        data: {
                            'flashcard_id': flashcard_id,                      
                            csrfmiddlewaretoken: csrf_token
                        },
                        url : '../ajax_show_comments',
                        success: function (data) {
                            $('#q_of_textarea_display').html(data.html);
                            $("#title_textarea_display").html("Commentaires");
 
                        }
                    }
                ) 

        });





        $('body').on('click', '.ajax_delete_flashcard',   function (event) { 
 
                let flashcard_id = $(this).data("flashcard_id");
                let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
                $.ajax(
                    {
                        type: "POST",
                        dataType: "json",
                        traditional: true,
                        data: {
                            'flashcard_id': flashcard_id,                      
                            csrfmiddlewaretoken: csrf_token
                        },
                        url : '../ajax_delete_flashcard',
                        success: function (data) {
                            $('#tr_flashchard'+flashcard_id).remove( );
                        }
                    }
                ) 

        });



    });
});