define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-exercise.js OK");

 

        // Affiche dans la modal la liste des élèves du groupe sélectionné
        $('select[name=level]').on('change', function (event) {
            let level_id = $(this).val();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
 
            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'level_id': level_id,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "ajax_theme_exercice",
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
        $('select[name=theme]').on('change', function (event) {
            let theme_id = $(this).val();
            let level_id = $('select[name=level]').val();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
 

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'theme_id': theme_id,
                        'level_id': level_id,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "ajax_knowledge_exercise",
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
                    }
                }
            )
        });

 
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
        $("#selector_student").click(function(){ 
            $('.selected_student').not(this).prop('checked', this.checked);
        });


        $('#enable_correction_div').hide();
        $("#enable_correction").click(function(){ 
            $('#enable_correction_div').toggle(500);
        });




        $("#id_is_python").on('change', function () { console.log("coucou");

            if ($("#id_is_python").is(":checked")) { $("#config_render").hide(500) ;}
            else { $("#config_render").show(500) ;}

        });


        $("#id_is_scratch").on('change', function () { console.log("coucou");

            if ($("#id_is_scratch").is(":checked")) { $("#config_render").hide(500) ;}
            else { $("#config_render").show(500) ;}

        });



        // Affiche dans la modal la liste des élèves du groupe sélectionné
        $('.choose_student').on('click', function (event) {

            let relationship_id = $(this).attr("data-relationship_id");
            let student_id = $(this).attr("data-student_id");
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            let custom = $(this).attr("data-custom");
            let parcours_id = $(this).attr("data-parcours_id"); 

            $("#id_student").val(student_id);
            $("#id_relationship").val(relationship_id);
            $("#id_parcours").val(parcours_id);
            $("#custom").val(custom);
 

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'student_id': student_id,
                        'custom' : custom ,
                        'relationship_id': relationship_id,
                        'parcours_id': parcours_id,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "../../ajax_choose_student",
                    success: function (data) {

                        $('#correction_div').html("").html(data.html);
                    }
                }
            )
         });






        // Corrige les élèves qui n'ont pas rendu de copie. Cela permet d'afficher la correction et de leur mettre une note.
        $('.exercise_no_made').on('click', function (event) {

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
 
        $("#id_is_realtime").on('change', function (){ 

            if ($(this).is(":checked")){

                $(".no_realtime").hide(500);
                $('#id_is_realtime').prop('checked', true); 
            } 
            else{

                $(".no_realtime").show(500);
                $('#id_is_realtime').prop('checked', false); 
            } 
        })
        ///////////////////////////////////////////
 


          
    $('.add_more').on('click', function (event) {

        var totalForms = parseInt(document.getElementById('id_customexercise_custom_answer_image-TOTAL_FORMS').value)  ;
        var FormToDuplicate = totalForms - 1 ;
 
        var tr_object = $('#duplicate').clone();
        tr_object.attr("id","duplicate"+totalForms) 
        tr_object.attr("style","display:block") 
        
        $(tr_object).find('.delete_button').html('<a href="javascript:void(0)" class="btn btn-danger remove_more">Supprimer</a>');

        $(tr_object).find('.btn-default').attr("name","customexercise_custom_answer_image-"+totalForms+"-image");
        $(tr_object).find('.btn-default').attr("id","customexercise_custom_answer_image-"+totalForms+"-image");


        tr_object.appendTo("#formsetZone");
        $("#id_customexercise_custom_answer_image-TOTAL_FORMS").val(totalForms+1)

    });



        $(document).on('click', '.remove_more', function () {
        var totalForms = parseInt(document.getElementById('id_customexercise_custom_answer_image-TOTAL_FORMS').value)  ;
        var FormToDuplicate = totalForms - 1 ;

            $('#duplicate'+FormToDuplicate).remove();
            $("#id_customexercise_custom_answer_image-TOTAL_FORMS").val(FormToDuplicate)
        });
                
 


        // Supprimer une image réponse depuis la vue élève.
        $('.delete_custom_answer_image').on('click', function () {

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
        $('.closer_exercise').on('click', function () {

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
        $('.correction_viewer').on('click', function () {

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

