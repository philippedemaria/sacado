define(['jquery', 'bootstrap', 'ui', 'ui_sortable'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-question-flash.js OK --");

        $('#id_is_display').prop('checked', false); 
        $('.div_is_mark').hide() ; 
        $(".div_is_ranking").hide(); 
        $(".div_time").hide();  
        $('#is_result_final').hide() ; 

        $('#id_is_publish').prop('checked', true); 
        $('#id_is_video').prop('checked', false); 
        $('#id_is_archive').prop('checked', false); 
        $('#id_is_mark').prop('checked', false); 
        $('#id_is_random').prop('checked', false); 
        $('#id_is_ranking').prop('checked', false); 
        $('#id_is_shuffle').prop('checked', false); 
        $('#id_is_back').prop('checked', false);
        $('#id_is_result').prop('checked', true);
        $('#id_is_share').prop('checked', false);
        $('#id_is_numeric').prop('checked', false);
        // $('#id_is_numeric').on('change', function (event) {
        //     $('.div_is_mark').toggle(300) ;
        //     $('#is_video_div').toggle(300) ;
        // });

        $('#id_is_result').on('change', function (event) {

             $('#is_result_final').toggle(300) ;  

        });

        $('#id_is_video').on('change', function (event) {
            $('.div_interslide').toggle(300) ;
        });

        $('#id_is_publish').on('change', function (event) {
            $('.div_time').toggle(300) ; 
        });

        $('.opener_k').hide() ;
        $('.opener_e').hide() ;
 
        $('body').on('click', '.opener' , function () { 
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
            let level_ids  = $("#id_levels").val();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            if ($("#is_questions_quizz").is(":checked")) {
                            is_quizz = true ;
                        } else {
                            is_quizz = false ;
                        }
 
            if(subject_id==''){ alert("Renseigner l'enseignement"); $('#is_questions_quizz').prop('checked', false); }

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",                    
                    traditional: true, // Permet d'envoyer une liste.
                    data: {
                        'subject_id'        : subject_id,
                        'level_ids'         : level_ids,
                        'is_questions_quizz': is_quizz,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "../ajax_select_style_questions",
                    success: function (data) {

                        $('#question_choice_style').html(data.html);
 
                    }
                }
            )
         });

 
        $('body').on('change', '#id_levels' , function (event) {  

            let subject_id = $("#id_subject").val();
            let level_ids  = $("#id_levels").val();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            if (!(level_ids)){ alert('Selectionner au moins un niveau.'); return false;}

            if ($("#is_questions_quizz").is(":checked")) {
                            is_quizz = true ;
                        } else {
                            is_quizz = false ;
                        }
 

            $("#question_choice_style").html("<i class='fa fa-spinner fa-pulse fa-fw fa-3x'></i>"); 

            if(subject_id==''){ alert("Renseigner l'enseignement"); $('#is_questions_quizz').prop('checked', false); }

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",                    
                    traditional: true, // Permet d'envoyer une liste.
                    data: {
                        'subject_id'        : subject_id,
                        'level_ids'         : level_ids,
                        'is_questions_quizz': is_quizz,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "../ajax_select_style_questions",
                    success: function (data) {

                        $('#question_choice_style').html("").html(data.html);
  
                    }
                }
            )
         });


        
        $('#create_questions_flash').prop('disabled', true);


        $('body').on('change', '.groupcheckbox' , function(event){               
                //on vérifie que nos conditions d'envoi sont bonnes
                if (countCheckedJQuery() >= 1){
                    $('#create_questions_flash').prop('disabled', false);
                }else
                {
                  $('#create_questions_flash').prop('disabled', true);  
                }
            });

        $('body').on('change', '.class_select_all_these_items' , function(event){               
                //on vérifie que nos conditions d'envoi sont bonnes
                $('#create_questions_flash').prop('disabled', false);
            });

             
            function countCheckedJQuery(){
                var checked = $(".groupcheckbox:checked");//sélectionne tous les éléments de classe "groupcheckbox" qui sont sélectionné
                return checked.length;
            }










    });
});