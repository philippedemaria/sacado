define(['jquery', 'bootstrap', 'ui', 'ui_sortable'], function ($) {
    $(document).ready(function () { 
        console.log("chargement JS ajax-support_exercise.js  OKK");


        //*************************************************************************************************************
        //********            ckEditor            **********************************************************************
        //*************************************************************************************************************
        CKEDITOR.replace('annoncement', {
                height: '200px',
                toolbar:    
                    [  
                        { name: 'clipboard',  items: [ 'Source', '-','Copy', 'Paste', 'PasteText' ] },
                        { name: 'paragraph',  items: [ 'NumberedList', 'BulletedList', '-',   'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock' ] }, 
                        { name: 'basicstyles',  items: [ 'Bold', 'Italic', 'Underline',  ] },
                        { name: 'insert', items: ['Image', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar','Iframe']},
                    ] ,
            });

        CKEDITOR.replace('correction', {
                height: '200px',
                toolbar:    
                    [  
                        { name: 'clipboard', items: [ 'Source', '-','Copy', 'Paste', 'PasteText' ] },
                        { name: 'paragraph', items: [ 'NumberedList', 'BulletedList', '-',   'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock' ] }, 
                        { name: 'basicstyles',  items: [ 'Bold', 'Italic', 'Underline',  ] },
                        { name: 'insert', items: ['Image', 'SpecialChar','Iframe']},   
                        { name: 'styles', items : [ 'Styles', 'TextColor','BGColor' ] },
                    ] ,
            });

        //*************************************************************************************************************
        //*************************************************************************************************************
        //*************************************************************************************************************  
        $('select[name=subject]').on('change', function (event) {
            let subject_id = $(this).val();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
 
            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'subject_id': subject_id,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "../../ajax_get_skills",
                    success: function (data) {
                        
                        skills = data["skills"]
                        $('select[name=skills]').empty("");
                        if (skills.length >0)
                        { 
                            for (let i = 0; i < skills.length; i++) {
                             
                                    let skills_id = skills[i][0];
                                    let skills_name =  skills[i][1]  ;
                                    let option = $("<option>", {
                                        'value': Number(skills_id),
                                        'html': skills_name
                                    });
                                    $('select[name=skills]').append(option);
                                }
                        }
                        else
                        {
                            let option = $("<option>", {
                                        'value': 0,
                                        'html': "Aucun contenu disponible"
                                        });
                            $('select[name=skills]').append(option);
                        }

                    }
                }
            )
        }); 



        $('select[name=level]').on('change', function (event) {
            let level_id   = $(this).val();
            let subject_id = $("#id_subject").val();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
 
            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'level_id'  : level_id,
                        'subject_id': subject_id,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "../../ajax_theme_exercice",
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
                    url: "../../ajax_knowledge_exercise",
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

        // Cache les div
        $('.no_visu').hide();

         
        // Gère l'affichage de la div des notes.
        if ($("#id_is_mark").is(":checked")) {$("#on_mark").show();} else { $("#on_mark").hide(); } 
 
     
        function clickDivAppear(toggle, $item) {
            $(document).on('click', toggle , function () {
                        $(".no_display").hide();        
                        $item.toggle(500);
                });
            }
 

        $(document).on('click', "#show_latex_formula" , function () {
                    $(".no_display").hide();        
                    $("#latex_formula").toggle(500);

                if ( $('.proposition').hasClass('no_visu_on_load')  )
                {   
                    $('.proposition').removeClass('no_visu_on_load') ;
                    $('.reponse').addClass('col-md-5') ;
                    $('.reponse').removeClass('col-md-12') ;
                    $(".qr").html("").html("un couple Question/Réponse");
                }
                else
                {   
                    $('.proposition').addClass('no_visu_on_load') ;
                    $('.reponse').removeClass('col-md-5') ;
                    $('.reponse').addClass('col-md-12') ;
                    $(".qr").html("").html("une valeur de la variable");
                }
            });



        // ==================================================================================================
        // =========    Gestion de l'aléatoire et du pseudo aléatoire    ====================================
        // ==================================================================================================   

        var open_situation_randomize       = 0 ;
        var open_situation_pseudorandomize = 0 ;
        $("#new_item").hide() ;
        $('body').on('click', '#show_randomize_zone' , function (event) { 
            $('#randomize_zone').toggle(500);
            $('#alert_variable').toggle(500);
            $("#new_item").toggle(500) ;
            if (open_situation_randomize%2==0)  {
                $('#nb_situation').show(500);  
                $('#show_pseudorandomize_zone').attr('id','no_show_pseudorandomize_zone') ; 
                $('#no_show_pseudorandomize_zone').attr('disabled',true) ; 
                $('.add_more').attr('disabled',true) ;
                $('#show_randomize_zone').remove() ;
            }
            else {
                $('#nb_situation').hide(500);  
                $('#no_show_pseudorandomize_zone').attr('id','show_pseudorandomize_zone') ;
                $('#show_pseudorandomize_zone').attr('disabled',false) ;
                $('.add_more').attr('disabled',false) ;
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

        // ==================================================================================================
        // ==================================================================================================
        // ==================================================================================================

 

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





        //*************************************************************************************************************
        //********      Gère le realtime         **********************************************************************
        //*************************************************************************************************************
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
        //*************************************************************************************************************
        //*************************************************************************************************************
        //*************************************************************************************************************  

        $(document).on('click', '.add_more_question', function (event) { 

                var total_form = $('#id_supportvariables-TOTAL_FORMS') ;
                var totalForms = parseInt(total_form.val())  ;

                var thisClone = $('#rowToClone_question');
                rowToClone = thisClone.html() ;

                $('#formsetZone_variables').append(rowToClone);
                $('#duplicate_variables').attr("id","duplicate_variables"+totalForms) 

                $('#duplicate_variables'+totalForms).find('.delete_button_question').html('<a href="javascript:void(0)" class="btn btn-danger remove_more_question" ><i class="fa fa-trash"></i></a>'); 
                $('#duplicate_variables'+totalForms).find("input[type='checkbox']").bootstrapToggle();

                $("#duplicate_variables"+totalForms+" input").each(function(){ 
                    $(this).attr('id',$(this).attr('id').replace('__prefix__',totalForms));
                    $(this).attr('name',$(this).attr('name').replace('__prefix__',totalForms));
                });
                total_form.val(totalForms+1);

                $("#id_situation").val(5);

            });


        $(document).on('click', '.remove_more_question', function () {
            var total_form = $('#id_supportvariables-TOTAL_FORMS') ;
            var totalForms = parseInt(total_form.val())-1  ;

            $('#duplicate_variables'+totalForms).remove();
            total_form.val(totalForms);

            if (totalForms==0) {$("#id_situation").val(1);}
        });



        $(document).on('click', '.add_more', function (event) { 

                var total_form = $('#id_supportchoices-TOTAL_FORMS') ;
                var totalForms = parseInt(total_form.val())  ;

                var thisClone = $('#rowToClone');
                rowToClone = thisClone.html() ;
                $('#formsetZone').append(rowToClone);
                $('#duplicate').attr("id","duplicate"+totalForms) 
                $('#imager').attr("id","imager"+totalForms) ;
                $('#file-image').attr("id","file-image"+totalForms) ;
                $('#feed_back').attr("id","feed_back"+totalForms)  ;       
                $('#div_feed_back').attr("id","div_feed_back"+totalForms)  ;
                $('#delete_img').attr("id","delete_img"+totalForms)  ;
                $('#duplicate'+totalForms).find('.delete_button').html('<a href="javascript:void(0)" class="btn btn-danger remove_more" ><i class="fa fa-trash"></i></a>'); 
                $('#duplicate'+totalForms).find("input[type='checkbox']").bootstrapToggle();
                $("#duplicate"+totalForms+" input").each(function(){ 
                    $(this).attr('id',$(this).attr('id').replace('__prefix__',totalForms));
                    $(this).attr('name',$(this).attr('name').replace('__prefix__',totalForms));
                });
                $("#duplicate"+totalForms+" textarea").each(function(){ 
                    $(this).attr('id',$(this).attr('id').replace('__prefix__',totalForms));
                    $(this).attr('name',$(this).attr('name').replace('__prefix__',totalForms));
                });
                $('#spanner').attr("id","spanner"+totalForms) ;
                $('#preview').attr("id","preview"+totalForms) ;
                total_form.val(totalForms+1);
            });



        $(document).on('click', '.remove_more', function () { 
            var total_form = $('#id_supportchoices-TOTAL_FORMS') ;
            var totalForms = parseInt(total_form.val())-1  ;

            $('#duplicate'+totalForms).remove();
            total_form.val(totalForms)
        });




        //*************************************************************************************************************  
        // Gestion des images des thèmes
        //************************************************************************************************************* 

        $('body').on('change', '.choose_imageanswer' , function (event) {
            var suffix = this.id.match(/\d+/); 
            previewFile(suffix) ;
         });  


        $('body').on('click', '.delete_img' , function (event) { 
                var suffix = this.id.match(/\d+/); 
                noPreviewFile(suffix) ;
                $(this).remove(); 
            });  


        function noPreviewFile(nb) {  
            $("#id_supportchoices-"+nb+"-imageanswer").attr("src", "" );
            $("#preview"+nb).val("") ;  
            $("#file-image"+nb).removeClass("preview") ;
            $("#preview"+nb).addClass("preview") ; 
            $("#id_supportchoices"+nb+"-imageanswer").removeClass("preview") ;
            $("#id_supportchoices-"+nb+"-answer").removeClass("preview") ;

          }

        function previewFile(nb) {

            const preview = $('#preview'+nb);
            const file = $('#id_supportchoices-'+nb+'-imageanswer')[0].files[0];
            const reader = new FileReader();
            $("#file-image"+nb).addClass("preview") ;
            $("#preview"+nb).val("") ;  
            $("#id_supportchoices-"+nb+"-answer").addClass("preview") ;
            $("#preview"+nb).removeClass("preview") ; 
            $("#delete_img"+nb).removeClass("preview") ; 

            reader.addEventListener("load", function (e) {
                                                var image = e.target.result ; 
                                                $("#preview"+nb).attr("src", image );
                                            }) ;

            if (file) { reader.readAsDataURL(file);}            

          }



        //*************************************************************************************************************  
        // FIN DE gestion
        //************************************************************************************************************* 




        // Chargement d'une image dans la réponse possible.
        $('body').on('click', '.automatic_insertion' , function (event) {  
 
            var feed_back = $(this).attr('id');
            $("#div_"+feed_back).toggle(500);

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


    $('body').on('mouseup', '.draggable' , function () {

        $('.quizz_item').css('border', '1px solid #E0E0E0'); 

        if ($('.select_items .quizz_choice').length == 1) { 

            $("#submit_button_relation").show()
        }
    })



    $( ".draggable" ).draggable({
            containment: ".dropzone",
            appendTo : '.droppable', 
            revert : true,
        });

    $( ".droppable" ).droppable({
            drop: function( event, ui ) {

                $(this).append( $(ui.draggable[0])  );
                this_answer = $(ui.draggable[0]).data("subchoice") ;
                old_list = $(this).find('input').val()  ;  
                var new_list = [];
                var new_str  = old_list +this_answer+"-";
                $(this).find('input').val(new_str);
                $('.quizz_item').css('border', '1px solid #E0E0E0');
            },
            over: function(event, ui) {
                $(this).css('border', '2px solid green');
            },
            out: function(event, ui) {

                this_answer = $(ui.draggable[0]).data("subchoice") ;
                old_list = $(this).find('input').val()  ;  
                var new_list = [];
                var new_str  = old_list.replace(this_answer+"-", "");
                $(this).find('input').val(new_str);
            }
    });



    $('body').on('mouseup', '.word_draggable' , function () {

        $('.quizz_item').css('border', '1px solid #E0E0E0'); 

        if ($('.select_items .word_choice').length == 1) { 
            $("#submit_button_relation").show()
        }
    })

    $( ".word_draggable" ).draggable({
            containment: ".dropzone",
            appendTo : '.input_droppable', 
            revert : true,
        });

    $( ".input_droppable" ).droppable({
            drop: function( event, ui ) {

                this_word = $(ui.draggable[0]).data("word") ;
                this_loop = $(this).data("loop") ; alert(this_loop) ;

                $(this).append( $(ui.draggable[0])  );
                $(this).css('border', '0px');
                $(this).css('vertical-align', 'normal');
                $(this).parent().find('.'+this_loop).val(this_word);

            },
            over: function(event, ui) {
            },
            out: function(event, ui) {
                $(this).css('border', '1px solid #E0E0E0');
                $(this).css('vertical-align', "");
            }
    });


    $(document).on('keyup','.secret_letter', function(e) { 
         
                  if (e.which == 32 || (65 <= e.which && e.which <= 65 + 25)
                                    || (97 <= e.which && e.which <= 97 + 25)
                                    || (192 == e.which) || (55 == e.which) || (50 == e.which)|| (57 == e.which) ) 
                    { 
                    
                        var c = String.fromCharCode(e.which) ;   
                        let csrf_token    = $("input[name='csrfmiddlewaretoken']").val();
                        let secret_letter = c ;
                        let nb_tries      = $("#nb_tries").val();
                        let index         = $(this).data('index');
                        let word_id       = $(this).data("word_id");
                        let word_id_used  =  $("#word_id_used").val();
                        let position      =  $("#position").val();
                        let word_length   =  $("#word_length").val();
                        let word_length_i =  $("#word_length_i").val();
                        let shuffle_ids   =  $("#shuffle_ids").val();
                        let used_letter   =  $("#used_letter").text(); 

                        $.ajax({
                                type: "POST",
                                dataType: "json",
                                data: {
                                    'secret_letter': secret_letter,
                                    'nb_tries'     : nb_tries,
                                    'word_id'      : word_id,
                                    'word_id_used' : word_id_used,
                                    'index'        : index,
                                    'position'     : position,
                                    'word_length'  : word_length,
                                    'shuffle_ids'  : shuffle_ids,
                                    'used_letter'  : used_letter,
                                    csrfmiddlewaretoken: csrf_token,
                                },
                                url: "../../ajax_secret_letter",
                                success: function (data) {
             
     
                                    if (data.response == "false")
                                    {   
                                        var new_position = parseInt(position) + 200;
                                        $("#position").val(new_position);
                                        $("#wordguess-counter").css("background-position","0 "+new_position+"px") ; 
                                        $("#secret_letter"+index).val('');
                                        $("#secret_letter"+index).focus() ;   
                                    }
                                    else {
                                        $("#secret_letter"+index).css('border','2px solid green');
                                        var nidx      = parseInt(index)+1;
                                        word_length_i = parseInt(word_length_i) ;
                                        if (parseInt(index)+1 < word_length_i){ $("#secret_letter"+nidx).focus(); } else {  $("#secret_letter0").focus(); } 
                                        $("#word_length").val(data.length);
                                    }

                                    $("#used_letter").text(data.used_letter);  
                                    if (data.win == "true")
                                    {   
                                        $("#word_id_used").val(data.word_id_used);   
                                        $("#"+data.input).val(data.word);
                                        $("#new_word").html("").html(data.new_word);
                                        $("#position").val(200);
                                        $("#word_length_i").val(data.length_i);
                                        $("#word_id").val(data.word_id);
                                        $("#used_letter").text("");
                                        $('#word_left').text(data.nb);
                                    }




                                
                                }
             
                            })

                    } 
            });



    var liste = [] ; 
    $(document).on('mousedown','#grid td', function(e) {  
     
            if ( $(this).hasClass("highlight") )
                {
                    $(this).removeClass("highlight") ;
                    idx = liste.indexOf(  $(this).text() ) ;
                    if(idx>-1)
                    { liste.splice(idx, 1) ;}
                }
            else
                {
                    $(this).addClass("highlight") ;
                    liste.push($(this).text());
                    text = liste.join("");
                    nb_words = $(".these_words").length ;
                    $(".these_words").each( function(index) {
                        if ( text == $("#word"+index).val() ){
                            $("#check"+index).html("<i class='fa fa-check text-success'></i>");
                            liste = [] ;
                        }
                    })
                }
        });


    var card_ids = [] ; 
    $(document).on('click','.card', function(e) {  
            
            let length     = $("#length").val();
            $(this).toggleClass('is-flipped');
            card_ids.push( $(this).data('id') ) ;

            if (card_ids.length == length){ setTimeout(function() {  test_ajax_memo(card_ids,length)}  , 1000) ;  }
                            
        }) 


    function test_ajax_memo(liste,length){

            let csrf_token  = $("input[name='csrfmiddlewaretoken']").val();
            let numexo      = $("#numexo").val();
            let score       = $("#score").val() ;

                $.ajax({
                        type: "POST",
                        dataType: "json",
                        traditional : true,
                        data: {
                            'liste' : liste,
                            'length': length,
                            csrfmiddlewaretoken: csrf_token,
                        },
                        url: "../../ajax_memo",
                        success: function (data) {

                              

                            if (data.test == "yes")
                            {
                                
                                $("#score_span").text( parseInt(score) + 1 );
                                $("#score").val( parseInt(score) + 1 );

                                $(".card").each( function(index) {
                                    if ( $(this).hasClass('is-flipped') ){
                                        $(this).addClass('card_open'); 
                                    }
                                })

                            }
                            else
                            {
                                $(".card").each( function(index) {
                                    if ( $(this).hasClass('is-flipped') ){
                                        $(this).removeClass('is-flipped');

                                    }
                                })
                            }
                            card_ids = [] ; console.log(card_ids) ;
                            $("#numexo_span").text( parseInt(numexo) + 1 );
                            $("#numexo").val( parseInt(numexo) + 1 );
                        }
                    }) 
    }
    // ****************************************************************************************************************************************
    // Gestion des slides dans la vue élève
    // ****************************************************************************************************************************************
    var this_slideBox = $('.this_slider ul');
    var slideWidth = 700 ;
    var slideQuantity = $('.this_slider ul').children('li').length;
    var currentSlide = 1 ;
    this_slideBox.css('width', slideWidth*slideQuantity);
    var nb_variables = $('#nb_variables').length; 

    //setTimeout( function() { set_var_value(1) }, 1000);


    $('.nav_start').on('click', function(){ 

            var pxValue = currentSlide * slideWidth ; 
            this_slideBox.animate({
                'left' : -pxValue
            });
            currentSlide++ ;
            //set_var_value(currentSlide) ;
    });

    // ****************************************************************************************************************************************
    // Gestion des variables aléatoires
    // ****************************************************************************************************************************************

    // function set_var_value(currentSlide) { 

    //     this_selector = "#this_slide"+currentSlide+" .MJXc-TeX-math-I" ; // emplacement de chaque variable  
    //     that_selector = "#this_slide"+currentSlide+" .quizz_item .MJXc-TeX-math-I" ;   
    //     var number ;
        
    //     $(".customvars").each( function(index) // pour chaque variable
    //     {     

    //         tab = $(this).val().split("=");  
    //         v          = tab[0];
    //         is_integer = tab[1];
    //         is_notnull = tab[2];
    //         max        = parseInt(tab[3]);
    //         min        = parseInt(tab[4]); 

    //         if (is_notnull){
    //             number = 0;
    //             while(number == 0){
    //                 if (is_integer){
    //                     number = min + Math.floor(Math.random() * (max-min) );    
    //                 }
    //                 else
    //                 {
    //                     number = min + Math.random() * (max-min);   
    //                 }
    //             }
    //         }
    //         else{
    //             if (is_integer){
    //                 number = min + Math.floor(Math.random() * (max-min) );    
    //             }
    //             else
    //             {
    //                 number = min + Math.random() * (max-min);   
    //             }
    //         }
 
    //         $(this_selector)[index].innerText = number ; // remplacement de la variable à chaque emplacement

    //         that_length = $(that_selector).length ;
    //         for(var i=0;i< that_length;i++){ // remplacement des variables dans les champs
    //             if ( $(that_selector)[i].innerText == v) { $(that_selector)[i].innerText =  number ; }
    //         }
    //     }) 
 
    //     $("#this_slide"+currentSlide+" .quizz_item .proposition").each(
    //         function(index){ 

    //             this_select = $("#this_slide"+currentSlide+" .quizz_item .proposition")[index] ;
    //             $("#this_slide"+currentSlide+" .quizz_item .proposition script").remove();
    //             $("#this_slide"+currentSlide+" .quizz_item .proposition .MJX_Assistive_MathML").remove();

    //             if( this_select.innerText.includes('calc:')) 
    //                 { 
    //                     this_select.innerText = this_select.innerText.replace('calc:',"").replace(/\n/g, "") ;
    //                     this_select.innerText = eval( this_select.innerText)     
    //                 }

    //         })
    //}
//*************************************************************************************************************  
// Gestion des solutions
//************************************************************************************************************* 

//*************************************************************************************************************  
// Récupération des réponses
//************************************************************************************************************* 

    $(document).on('change', ".selected_answer" , function () { 

        let csrf_token     = $("input[name='csrfmiddlewaretoken']").val();
        let supportfile_id = $(this).data("supportfile_id") ;
        let is_correct     = $(this).data("is_correct") ;
        let loop           = $(this).data("loop") ;
        let choice_id      = $(this).val() ;
        let list_choices   = [] ;   
             
        if ($(this).is(":checked"))
        {
            list_choices.push(choice_id) ;
        }
        else{

            idx = list_choices.indexOf(  choice_id ) ;
            if(idx>-1)
            { list_choices.splice(idx, 1) ;}
        }
        $("#nav_start"+loop).attr("data-choice_ids",list_choices);
        $("#nav_start"+loop).attr("data-supportfile_id",supportfile_id);
        $("#nav_start"+loop).attr("data-is_correct",is_correct);
    });



//*************************************************************************************************************  
// Récupération des Vrai/Faux
//************************************************************************************************************* 

    $(document).on('click', ".show_this_vf_correction" , function () {

            let csrf_token     = $("input[name='csrfmiddlewaretoken']").val();
            let choice_ids     = $(this).data("choice_ids") ;
            let score          = $("#score").val();
            let numexo         = $("#numexo").val();
            let is_correct     = $(this).data("is_correct") ;

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    traditional : true,
                    data: {
                        'is_correct': is_correct,
                        'choice_ids': choice_ids, 
                        'numexo'    : numexo,
                        'score'     : score, 
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "../../check_solution_vf",
                    success: function (data) {
                        $("#score").val(data.score);
                        $("#numexo").val(data.numexo);
                        $("#score_span").html(data.score);
                        $("#numexo_span").html(data.numexo);
                        $("#this_correction_text").html(data.this_correction_text);
                        $("#message_correction").html(data.msg);   
                        MathJax.Hub.Queue(["Typeset",MathJax.Hub]);    
                    }
                }
            )
         });

//*************************************************************************************************************  
// Correction des QCM
//************************************************************************************************************* 

    $(document).on('click', ".show_this_qcm_correction" , function () {

            let csrf_token     = $("input[name='csrfmiddlewaretoken']").val();
            let supportfile_id = $(this).data("supportfile_id") ;
            let choice_ids     = $(this).data("choice_ids") ;
            let loop           =  $(this).data("loop") ;
            let score          = $("#score").val();
            let numexo         = $("#numexo").val();


            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    traditional : true,
                    data: {
                        'supportfile_id': supportfile_id,
                        'choice_ids'       : choice_ids, 
                        'numexo'           : numexo,
                        'score'            : score, 
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "../../check_solution_qcm_numeric",
                    success: function (data) {

                        $("#show_correction"+loop).show(500);
                        $("#score").val(data.score);
                        $("#numexo").val(data.numexo);
                        $("#score_span").html(data.score);
                        $("#numexo_span").html(data.numexo);
                        $("#this_correction_text"+loop).html(data.this_correction_text);
                        $("#message_correction"+loop).html(data.msg);  
                        $("#message_correction"+loop).html(data.msg);  
                        MathJax.Hub.Queue(["Typeset",MathJax.Hub]);    
                    }
                }
            )
         });
 
 
 
//*************************************************************************************************************  
// Correction des réponses à compléter
//************************************************************************************************************* 
  
    $(document).on('click', ".show_these_inputs_correction" , function (event) {
 

            event.preventDefault();   
            my_form = document.querySelector("#all_types_form");
            var form_data = new FormData(my_form); 
 
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            form_data.append("csrfmiddlewaretoken" , csrf_token);

            let supportfile_id = $(this).data("supportfile_id") ;
            let loop           = $(this).data("loop") ;
            let choice_id      = $(this).data("choice_id") ;
            form_data.append("supportfile_id" , supportfile_id); 
            form_data.append("loop" , loop); 
            form_data.append("choice_id" , choice_id); 

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    traditional : true,
                    data: form_data,
                    url: "../../check_solution_answers",
                    success: function (data) {
                        $("#score").val(data.score);
                        $("#numexo").val(data.numexo);
                        $("#score_span").html(data.score);
                        $("#numexo_span").html(data.numexo);
                        $("#this_correction_text").html(data.this_correction_text);
                        $("#message_correction").html(data.msg);     
                        MathJax.Hub.Queue(["Typeset",MathJax.Hub]);    
                    },
                        cache: false,
                        contentType: false,
                        processData: false
                }
            )
         });


 

});

});

 
