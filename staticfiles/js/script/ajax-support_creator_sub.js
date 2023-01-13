define(['jquery', 'bootstrap', 'ui', 'ui_sortable','ckeditor'], function ($) {
    $(document).ready(function () { 
        console.log("chargement JS ajax-support_creator_sub.js");


        //**************************************************************************************************************
        //********            ckEditor            **********************************************************************
        //**************************************************************************************************************
        if ( $('#qtype').val() == '2' ) {  cke_height = '250px' ;} else {  cke_height = '100px' ;}

        CKEDITOR.replace('annoncement', {
                height: cke_height ,
                toolbar:    
                    [  
                        { name: 'clipboard',  items: [ 'Source'] },
                        { name: 'paragraph',  items: [ 'NumberedList', 'BulletedList', '-',   'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock' ] }, 
                        { name: 'basicstyles',  items: [ 'Bold', 'Italic', 'Underline',  ] },
                        { name: 'insert', items: ['Image', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar','Iframe']},
                    ] ,
            });

        CKEDITOR.replace('correction', {
                height: cke_height,
                toolbar:    
                    [  
                        { name: 'clipboard', items: [ 'Source'] },
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


    $("#id_title").val("Regrouper les cartes par thèmes");


        //*************************************************************************************************************  
        // Gestion des variables dynamiques
        //************************************************************************************************************* 

        $(document).on('click', '.add_more_question', function (event) { alert();

                var total_form = $('#id_customvariables-TOTAL_FORMS') ;
                var totalForms = parseInt(total_form.val())  ;

                var thisClone = $('#rowToClone_question');
                rowToClone = thisClone.html() ;

                $('#formsetZone_variables').append(rowToClone);
                $('#duplicate_variables').attr("id","duplicate_variables"+totalForms) 
                //$('#cloningZone').attr("id","cloningZone"+totalForms) 

                $('#duplicate_variables'+totalForms).find('.delete_button_question').html('<a href="javascript:void(0)" class="btn btn-danger remove_more_question" ><i class="fa fa-trash"></i></a>'); 
                $('#duplicate_variables'+totalForms).find("input[type='checkbox']").bootstrapToggle();

                $("#duplicate_variables"+totalForms+" input").each(function(){ 
                    $(this).attr('id',$(this).attr('id').replace('__prefix__',totalForms));
                    $(this).attr('name',$(this).attr('name').replace('__prefix__',totalForms));
                });
                total_form.val(totalForms+1);

            });


        $(document).on('click', '.remove_more_question', function () {
            var total_form = $('#id_customvariables-TOTAL_FORMS') ;
            var totalForms = parseInt(total_form.val())-1  ;

            $('#duplicate_variables'+totalForms).remove();
            total_form.val(totalForms)
        });

        //*************************************************************************************************************  
        // Gestion des thèmes
        //************************************************************************************************************* 

        $(document).on('click', '.add_more', function (event) {

                var supportchoices       = $('#id_supportchoices-TOTAL_FORMS') ;
                var total_supportchoices = parseInt( supportchoices.val() ) ;
                $("#nb_pseudo_aleatoire").html("").html(total_supportchoices+1);
                var thisClone = $('#rowToClone');
                rowToClone = thisClone.html() ;

                $('#formsetZone').append(rowToClone);

                $('#duplicate').attr("id","duplicate"+total_supportchoices) ;
                $('#cloningZone').attr("id","cloningZone"+total_supportchoices) ;
                $('#imager').attr("id","imager"+total_supportchoices) ;
                $('#file-image').attr("id","file-image"+total_supportchoices) ;
                $('#feed_back').attr("id","feed_back"+total_supportchoices)  ;       
                $('#div_feed_back').attr("id","div_feed_back"+total_supportchoices)  ;
                $('#delete_img').attr("id","delete_img"+total_supportchoices)  ;
                $('#data_loop').attr("data-loop", total_supportchoices)  ;
                $('#data_loop').attr("id","data_loop"+total_supportchoices)  ;


                if( $('#imagerbis').length ) { 
                    $('#imagerbis').attr("id","imagerbis"+total_supportchoices) ; 
                    $('#file-imagebis').attr("id","file-imagebis"+total_supportchoices) ;
                    $('#preview_bis').attr("id","preview_bis"+total_supportchoices) ;
                    $('#delete_imgbis').attr("id","delete_imgbis"+total_supportchoices)  ;
                } 
                $('#subformsetZone').attr("id","subformsetZone"+total_supportchoices)  ;

                if( $('#imagersub').length ) { 

                    l_items = $("#subformsetZone"+total_supportchoices+" .get_image").length ; 
                    for(var i = 0;i<l_items;i++ ){
                        var suf = "-"+total_supportchoices+'_'+i ; 
                        $('#imagersub').attr("id","imagersub"+suf) ;
                        $('#file-imagesub').attr("id","file-imagesub"+suf) ;
                        $('#previewsub').attr("id","previewsub"+suf) ;
                        $('#delete_subimg').attr("id","delete_subimg"+suf)  ;
                    }

                    this_selector = $("#subformsetZone"+total_supportchoices+" input"); 
                    new_attr_id = this_selector.attr("id")+suf  ;
                    new_attr_nm = this_selector.attr("name")+suf  ;
                    this_selector.attr("data-loop",suf);                        
                    this_selector.attr("id",new_attr_id);
                    this_selector.attr("name",new_attr_nm);

                    this_answer = $("#subformsetZone"+total_supportchoices+" textarea"); 
                    new_attr_id = this_answer.attr("id")+suf  ;
                    new_attr_nm = this_answer.attr("name")+suf  ;
                    this_answer.attr("data-loop",suf);                        
                    this_answer.attr("id",new_attr_id);
                    this_answer.attr("name",new_attr_nm);
                } 
                
                $("#supportchoices-"+total_supportchoices+"-is_correct").prop("checked", false); 

                $("#duplicate"+total_supportchoices+" input").each(function(index){ 
                    $(this).attr('id',$(this).attr('id').replace('__prefix__',total_supportchoices));
                    $(this).attr('name',$(this).attr('name').replace('__prefix__',total_supportchoices));
                });

                $('#duplicate'+total_supportchoices).find("input[type='checkbox']").bootstrapToggle();
 
                $("#duplicate"+total_supportchoices+" textarea").each(function(){ 
                    $(this).attr('id',$(this).attr('id').replace('__prefix__',total_supportchoices));
                    $(this).attr('name',$(this).attr('name').replace('__prefix__',total_supportchoices));
                });
 

                $('#spanner').attr("id","spanner"+total_supportchoices) ;
                $('#preview').attr("id","preview"+total_supportchoices) ;

                $('#subloop'+total_supportchoices).val(0) ;

                supportchoices.val(total_supportchoices+1);
            });



        $(document).on('click', '.remove_more', function () {
            
            var supportchoices = $('#id_supportchoices-TOTAL_FORMS') ;
            var total_supportchoices = parseInt( supportchoices.val() )-1  ;

            $('#duplicate'+total_supportchoices).remove();
            supportchoices.val(total_supportchoices);
            $("#nb_pseudo_aleatoire").html("").html(total_supportchoices);
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
            $("#imager"+nb).addClass("col-sm-2 col-md-1").removeClass("col-sm-4 col-md-3");
            $("#imager"+nb).next().addClass("col-sm-10 col-md-11").removeClass("col-sm-8 col-md-9");

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
            $("#imager"+nb).removeClass("col-sm-2 col-md-1").addClass("col-sm-4 col-md-3");
            $("#imager"+nb).next().removeClass("col-sm-10 col-md-11").addClass("col-sm-8 col-md-9");

            reader.addEventListener("load", function (e) {
                                                var image = e.target.result ; 
                                                $("#preview"+nb).attr("src", image );
                                            }) ;

            if (file) { reader.readAsDataURL(file);}            

          }



        //*************************************************************************************************************  
        // Gestion des sous thèmes
        //************************************************************************************************************* 


        var ntotal_form = $('#id_supportsubchoices-TOTAL_FORMS') ;
        var ntotalForms = parseInt(ntotal_form.val())  ;

        for (n=0;n<ntotalForms;n++){

            $('#subformsetZone'+n+" .to-data-loop").each( function( index ) {
                      $(this).attr('data-loop',n+"_"+index);
                      $(this).attr('id',$(this).attr('id')+n+"_"+index);
                      $(this).attr('name',$(this).attr('name')+n+"_"+index);
                    });

            $("#subformsetZone"+n+" textarea").each(function(index){ 
                $(this).attr('name',$(this).attr('name')+n+"_"+index);
                $(this).attr('id',$(this).attr('id')+n+"_"+index);
            });
        }
 

        $(document).on('click', '.add_sub_more', function (event) { 

                var thisClone = $('#subToClone');
                subToClone = thisClone.html() ;

                loop = $(this).attr("data-loop");
                subloop = $('#subloop'+loop).val()
                var suffixe = loop+"_"+subloop ;

                $('#subformsetZone'+loop).append(subToClone);

                $('#subduplicate').attr("id","subduplicate"+suffixe) ;
                $('#imagersub').attr("id","imagersub"+suffixe)    ;
                $('#file-imagesub').attr("id","file-imagesub"+suffixe);
                $('#delete_subimg').attr("id","delete-subimg"+suffixe);

                $("#subduplicate"+suffixe+" input").each(function(){                  
                    $(this).attr('id',$(this).attr('id').replace('__prefix__',subloop));
                    $(this).attr('name',$(this).attr('name').replace('__prefix__',subloop));
                    $(this).attr('data-loop', suffixe) ;
                    $(this).attr('id',$(this).attr('id')+suffixe);
                    $(this).attr('name',$(this).attr('name')+suffixe);
                });

                $("#subduplicate"+suffixe+" textarea").each(function(){ 
                    $(this).attr('id',$(this).attr('id').replace('__prefix__',subloop));
                    $(this).attr('name',$(this).attr('name').replace('__prefix__',subloop));
                    $(this).attr('name',$(this).attr('name')+suffixe);
                    $(this).attr('id',$(this).attr('id')+suffixe);
                });

                $('#spanner').attr("id","spanner"+suffixe) ;
                $('#previewsub').attr("id","previewsub"+suffixe) ;

                var subloop_int = parseInt( subloop )  ;  

                $('#subloop'+loop).val( subloop_int + 1 );  
                $("#subduplicate"+suffixe).find("span").attr('data-suffixe',suffixe)

            });



        $(document).on('click', '.remove_sub_more', function () {
 
            suffixe = $(this).data("suffixe") ; 
            loop = suffixe.split("_")[0];
            $('#subloop'+loop).val(    parseInt($('#subloop'+loop).val())-1 );
            $('#subduplicate'+suffixe).remove();

        });


        $(document).on('click', '.automatic_insertion' , function (event) {  
            var feed_back = $(this).attr('id');
            $("#div_"+feed_back).toggle(500);
         });



        //*************************************************************************************************************  
        // Gestion des images des sous thèmes
        //*************************************************************************************************************  
        $('body').on('change', '.choose_imageanswersub' , function (event) { alert() ;

            var loop       = $(this).data("loop"); // le loop est composé du loop parent et du subloop dans cet ordre : 1-0 est le loop parent 1 et le subloop 0
            SubpreviewFile(loop) ;
         });  


        $('body').on('click', '.delete_subimg' , function (event) { 
                var suffix = this.id.match(/\d+/); 
                var loop   = $(this).attr('id').substring(13);
                SubnoPreviewFile(loop) ;
                $(this).remove(); 
            });  


        function SubnoPreviewFile(loop) { 
            let nb  = loop.split("_")[1];

            if (nb<2)
            { loop = loop.replace("-","");}

            $("#id_supportsubchoices-"+nb+"-imageanswer"+loop).val();
            $("#id_supportsubchoices-"+nb+"-imageanswer"+loop).removeAttr("src");
            $("#id_supportsubchoices"+nb+"-imageanswer"+loop).removeClass("preview") ;
            $("#id_supportsubchoices-"+nb+"-answer"+loop).removeClass("preview") ; 
                       
            $("#previewsub"+loop).removeAttr("src");
            $("#previewsub"+loop).addClass("preview") ; 
            $("#file-imagesub"+loop).removeClass("preview") ;

            $("#imagersub"+loop).addClass("col-sm-2 col-md-1").removeClass("col-sm-4 col-md-3");
            $("#imagersub"+loop).next().addClass("col-sm-10 col-md-11").removeClass("col-sm-8 col-md-9");
          }

        function SubpreviewFile(loop) {

            let nb  = loop.split("_")[1];
            
            if (nb<2) { loop = loop.replace("-",""); } 
 
            const file = $('#id_supportsubchoices-'+nb+'-imageanswer'+loop)[0].files[0];
            const reader = new FileReader();

            console.log(nb) ;
            console.log(loop) ;
            console.log(file) ;

            $("#file-imagesub"+loop).addClass("preview") ; 
            $("#id_supportsubchoices"+nb+"-answer-"+loop).addClass("preview") ;
            $("#previewsub"+loop).removeClass("preview") ; 
            $("#imagersub"+loop).removeClass("col-sm-2 col-md-1").addClass("col-sm-4 col-md-3");
            $("#imagersub"+loop).next().removeClass("col-sm-10 col-md-11").addClass("col-sm-8 col-md-9");
            $("#imagersub"+loop).next().append('<a href="javascript:void()" id="delete_subimg'+loop+'" class="delete_subimg"><i class="fa fa-trash"></i></a>');

            reader.addEventListener("load", function (e) {
                                                var image = e.target.result ; 
                                                $("#previewsub"+loop).attr("src", image );
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



 

});

});

 
