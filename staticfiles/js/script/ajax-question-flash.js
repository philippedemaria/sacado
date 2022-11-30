define(['jquery', 'bootstrap', 'ui', 'ui_sortable'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-question-flash.js OK --");



        $('.opener_k').hide() ;
        $('.opener_e').hide() ;
 

        $('.opener').on('click' ,function () { 
            $('.opener_k').hide() ;

            if( $(this).hasClass("out") )
            {
                $(".opener ~ .opened"+this.id).show();
                $(this).removeClass("out").addClass("in");
                $(this).find('.fa').removeClass('fa-caret-right').addClass('fa-caret-down');
            }
            else 
            {
                $(".opener ~ .opened"+this.id).hide();  
                $(this).removeClass("in").addClass("out"); 
                $(this).find('.fa').removeClass('fa-caret-down').addClass('fa-caret-right'); 
            }
 
        });

 
        $('body').on('change', '#is_questions_quizz' , function (event) {  

            let subject_id = $("#id_subject").val();
            let is_questions_quizz = $("#is_questions_quizz").val();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'subject_id'        : subject_id,
                        'is_questions_quizz': is_questions_quizz,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "../ajax_select_style_questions",
                    success: function (data) {

                        $('#question_choice_style').html(data.html);
 
                    }
                }
            )
         });







    });
});