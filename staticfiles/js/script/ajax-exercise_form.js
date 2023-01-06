define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-exercise_form.js OK");

        // Affiche dans la modal la liste des élèves du groupe sélectionné
        $('#id_level').on('change', function (event) {

            let subject_id = $('#id_subject').val();            
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            let level_ids  = $(this).val();

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    traditional : true,
                    data: {
                        'subject_id': subject_id,
                        'level_ids' : level_ids,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "../ajax_theme_subject_levels",
                    success: function (data) {

                        $('select[name=theme]').html("");
                        // Remplir la liste des choix avec le résultat de l'appel Ajax
                        let themes = JSON.parse(data["themes"]);
                        for (let i = 0; i < themes.length; i++) {

                            let theme_id = themes[i].pk;
                            let name =  themes[i].fields['name'];
                            let option = $("<option>", {
                                'value': Number(theme_id),
                                'html': name
                            });
                            $('#id_theme').append(option);
                        } 
                    }
                }
            )
        });


        // Affiche dans la modal la liste des élèves du groupe sélectionné
        $('.knowledge_skills').on('change', function (event) {

            let subject_id = $('#id_subject').val();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            let level_ids  = $('#id_level').val();
            let theme_ids  = $('#id_theme').val();

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    traditional : true,
                    data: {
                        'subject_id': subject_id,
                        'theme_ids' : theme_ids,
                        'level_ids' : level_ids,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "../ajax_knowledge_skills_subject_levels",
                    success: function (data) {
                        $('select[name=knowledge]').html("");
                        // Remplir la liste des choix avec le résultat de l'appel Ajax
                        let knowledges = JSON.parse(data["knowledges"]);
                        for (let i = 0; i < knowledges.length; i++) {

                            let knowledge_id = knowledges[i].pk;
                            let name =  knowledges[i].fields['name'];
                            let option = $("<option>", {
                                'value': Number(knowledge_id),
                                'html': name
                            });
                            $('#id_knowledge').append(option);
                        }
                        $('select[name=skills]').html("");
                        // Remplir la liste des choix avec le résultat de l'appel Ajax
                        let skills = JSON.parse(data["skills"]);
                        for (let i = 0; i < skills.length; i++) {

                            let skill_id = skills[i].pk;
                            let name =  skills[i].fields['name'];
                            let option = $("<option>", {
                                'value': Number(skill_id),
                                'html': name
                            });
                            $('#id_skills').append(option);

                        }
                    }
                }
            )
        });


        var open_situation_randomize       = 0 ;
        var open_situation_pseudorandomize = 0 ;

        $('body').on('click', '#show_randomize_zone' , function (event) { 
            $('#randomize_zone').toggle(500);
            if (open_situation_randomize%2==0)  {
                $('#nb_situation').show(500);  
                $('#show_pseudorandomize_zone').attr('id','no_show_pseudorandomize_zone') ; 
                $('#no_show_pseudorandomize_zone').attr('disabled',true) ; 
                $('.add_more').attr('disabled',true) ;

                $('.proposition').addClass('no_visu_on_load') ;
                $('.reponse').removeClass('col-md-5') ;
                $('.reponse').addClass('col-md-12') ;
            }
            else {
                $('#nb_situation').hide(500);  
                $('#no_show_pseudorandomize_zone').attr('id','show_pseudorandomize_zone') ;
                $('#show_pseudorandomize_zone').attr('disabled',false) ;

                $('.add_more').attr('disabled',false) ;
                $('.proposition').removeClass('no_visu_on_load') ;
                $('.reponse').removeClass('col-md-12') ;
                $('.reponse').addClass('col-md-5') ;
            }
            open_situation_randomize +=1 ;

         });

        $('body').on('click', '#show_pseudorandomize_zone' , function (event) { 
            if (open_situation_pseudorandomize%2==0)
                {  
                    $('#nb_situation').show(500);
                    $('#show_randomize_zone').attr('id','no_show_randomize_zone') ; 
                    $('#no_show_randomize_zone').attr('disabled',true) ;  
                }
            else 
                {$('#nb_situation').hide(500);
                 $('#no_show_randomize_zone').attr('id','show_randomize_zone') ; 
                 $('#show_randomize_zone').attr('disabled',false) ;
             }
            open_situation_pseudorandomize +=1 ;
         });


        // ******************************************************************************************************************************
        // ******************************************************************************************************************************
        // animation des div du socle et des types d'exos
        // ******************************************************************************************************************************
        var height = $('#full_socle_div').height() ;
        var height_ = $('#full_kind_exercise_div').height() ;

        $('#up_and_down_socle_div').on('click', function (event) { 
            up_and_down('#socle_div','#up_and_down_socle_div',height)
        });

        $('#up_and_down_kind_exercise_div').on('click', function (event) { 
            up_and_down('#kind_exercise_div','#up_and_down_kind_exercise_div', height_)
        });

        function up_and_down(id_div,selector,height){
            if ( $(id_div+' .row').hasClass('no_visu_on_load') ){
            $(id_div).animate({ height : height_+"px"}, 500);
            $(id_div+' .row').removeClass('no_visu_on_load'); 
            $(selector).html('<i class="fa fa-caret-up"></i></a>'); 
            }
            else {
            $(id_div).animate({ height : "70px"}, 500);
            $(id_div+' .row').addClass('no_visu_on_load');  
            $(selector).html('<i class="fa fa-caret-down"></i></a>');             
            }
        }
        // ******************************************************************************************************************************
        // ******************************************************************************************************************************
        // ******************************************************************************************************************************
 
        $(".setup_no_ggb").hide();
            makeItemAppear($("#id_is_ggbfile"), $(".setup_ggb"), $(".setup_no_ggb"));
            function makeItemAppear($toggle, $item, $itm) {
                    $toggle.change(function () {
                        if ($toggle.is(":checked")) {
                            $item.show(500);
                            $itm.hide(500);

                        } else {
                            $item.hide(500);
                            $itm.show(500);
                            }
                    });
                }


            $("#collaborative_div").hide();
            makeDivAppear($("#id_is_text"), $("#collaborative_div"));
            makeDivAppear($("#id_is_mark"), $("#on_mark"));
            makeDivAppear($("#id_is_autocorrection"), $("#positionnement"));

            function makeDivAppear($toggle, $item) {
                    $toggle.change(function () {
                        if ($toggle.is(":checked")) {
                            $item.show(500);

                        } else {
                            $item.hide(500);
                            }
                    });
                }

 

        // Gère les notes.
        if ($("#id_is_mark").is(":checked"))
            {
                $("#on_mark").show();
            } 
        else{
                $("#on_mark").hide();
            } 

        ///////////////////////////////////////////
        $(document).on('click', "#selector_student", function () {
            $('.selected_student').not(this).prop('checked', this.checked);
        });


        $('#enable_correction_div').hide();
        $(document).on('click', "#enable_correction", function () {
            $('#enable_correction_div').toggle(500);
        });




        $(document).on('change', "#id_is_python", function () { 

            if ($("#id_is_python").is(":checked")) { $("#config_render").hide(500) ;}
            else { $("#config_render").show(500) ;}

        });
 

        // Corrige les élèves qui n'ont pas rendu de copie. Cela permet d'afficher la correction et de leur mettre une note.
        $(document).on('click','.exercise_no_made', function (event) {

            let exercise_id = $(this).attr("data-exercise_id");
            let student_id = $(this).attr("data-student_id");
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            let custom = $(this).attr("data-custom");
            let parcours_id = $(this).attr("data-parcours_id"); 
 

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'student_id': student_id,
                        'custom' : custom ,
                        'exercise_id': exercise_id,
                        'parcours_id': parcours_id,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "../../../ajax_annotate_exercise_no_made",
                    success: function (data) {

                        $('#exercise_no_made'+student_id).html("<i class='fa fa-toggle-on text-success pull-right'></i>");
                    }
                }
            )
         });



        // Gère le realtime.
        if ($("#id_is_realtime").is(":checked")){

                $(".no_realtime").hide();

            } 
        else{

                $(".no_realtime").show();

            } 
 
        $(document).on('change',"#id_is_realtime", function (){ 

            if ($(this).is(":checked")){

                $(".no_realtime").hide(500);
                $('#id_is_realtime').prop('checked', true); 
            } 
            else{

                $(".no_realtime").show(500);
                $('#id_is_realtime').prop('checked', false); 
            } 
        })
        //====================================================================================
        //====================================================================================
        //====================================================================================

   

        // Supprimer une image réponse depuis la vue élève.
        $('body').on('click', '.delete_custom_answer_image', function () {

            let image_id = $(this).attr("data-image_id");
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            let custom = $(this).attr("data-custom");

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'image_id': image_id,
                        'custom' : custom,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "../../ajax_delete_custom_answer_image",
                    success: function (data) {

                        $("#delete_custom_answer_image"+image_id).remove();
                    }
                }
            )
         });

 


        // Supprimer une image réponse depuis la vue élè
        $('body').on('click', '.closer_exercise', function () {

            let exercise_id = $(this).attr("data-exercise_id");

            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            let custom = $(this).attr("data-custom");

            if (custom == "0" ) { var parcours_id = $(this).attr("data-parcours_id"); } else { var parcours_id = 0 ; }

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'exercise_id': exercise_id,
                        'parcours_id': parcours_id,
                        'custom' : custom,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "../../../ajax_closer_exercise",
                    success: function (data) {
 
                        $("#closer").html(data.html);

                        $(".closer_exercise").removeClass(data.btn_off).addClass(data.btn_on);

                    }
                }
            )
         });




        // Supprimer une image réponse depuis la vue élè
        $('body').on('click', '.correction_viewer' ,function () {

            let exercise_id = $(this).attr("data-exercise_id");

            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            let custom = $(this).attr("data-custom");

            if (custom ==  1  ) { var parcours_id = $(this).attr("data-parcours_id"); } else { var parcours_id = 0 ; }

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'exercise_id': exercise_id,
                        'parcours_id': parcours_id,
                        'custom' : custom,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "../../../ajax_correction_viewer",
                    success: function (data) {
 
                        $("#showing_cor").html(data.html);

                        $(".correction_viewer").removeClass(data.btn_off).addClass(data.btn_on);

                    }
                }
            )
         });

      


        // Supprimer une image réponse depuis la vue élève.
        $('body').on('click', '#click_more_criterion_button' , function () {

            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
 
            let label=$("#id_label").val() ;
            let skill= $("#id_skill").val() ;
            let knowledge = $("#id_knowledge").val() ;
            let subject = $("#id_subject").val() ;
            let level = $("#id_level").val() ;

 
            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'label': label,
                        'skill': skill,
                        'knowledge': knowledge,
                        'subject': subject,
                        'level' : level,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "../../ajax_add_criterion",
                    success: function (data) {
 
 

                        criterions = data["criterions"] ; 
                        $('#id_criterions').empty("");

                        for (let i = 0; i < criterions.length ; i++) {
                                    
                                let criterions_id = criterions[i][0]; 
                                let criterions_name =  criterions[i][1] ; 
 
                                $('#id_criterions').append('<label for="id_criterions_'+Number(criterions_id)+'"><input type="checkbox" id="id_criterions_'+Number(criterions_id)+'" name="criterions" value="'+Number(criterions_id)+'" /> '+criterions_name+'</label><br/>')
                            }

                    }
 
                }
            )
         });


        // Supprimer une image réponse depuis la vue élève.
        $('body').on('click', '.auto_evaluate' , function () {

            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            let customexercise_id= $(this).data("customexercise_id") ;
            let criterion_id     = $(this).data("criterion_id") ;
            let parcours_id      = $(this).data("parcours_id") ;
            let student_id       = $(this).data("student_id") ;
            let position         = $(this).val() ;
 
            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'customexercise_id': customexercise_id,
                        'criterion_id': criterion_id,
                        'parcours_id': parcours_id,
                        'student_id': student_id,
                        'position'  : position , 
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "../../ajax_auto_evaluation",
                    success: function (data) {
 
                        $("#auto_eval"+criterion_id).html("<i class='fa fa-check text-success'></i>") ;

                    }
 
                }
            )
         });



});

});

