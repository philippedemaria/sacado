define(['jquery','bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-parcours.js OK");

        $(".is_evaluation").attr("checked",false);

        // ================================================================ 
        // Parcours menu vertical pour les cours
        var navItems = $('.admin-menu li > a');
        var navListItems = $('.admin-menu li');
        var allWells = $('.admin-content');
        var allWellsExceptFirst = $('.admin-content:not(:first)');
        allWellsExceptFirst.hide();
        navItems.click(function(e)
        {
            e.preventDefault();
            navListItems.removeClass('active');
            $(this).closest('li').addClass('active');
            
            allWells.hide();
            var target = $(this).attr('data-target-id');
            $('#' + target).show();
        });
        // ================================ FIN ============================ 

        // Affiche dans la modal la liste des élèves du groupe sélectionné
        $('#id_level').on('change', function (event) {
            let id_level = $(this).val();
            let id_subject = $("#id_subject").val();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    traditional: true,
                    data: {
                        'id_level': id_level,
                        'id_subject': id_subject,                        
                        csrfmiddlewaretoken: csrf_token
                    },
                    url : "../../ajax/chargethemes",
                    success: function (data) {

                        themes = data["themes"]
                        $('select[name=theme]').empty("");
                        if (themes.length >0)

                        { for (let i = 0; i < themes.length; i++) {
                                    

                                    console.log(themes[i]);
                                    let themes_id = themes[i][0];
                                    let themes_name =  themes[i][1]  ;
                                    let option = $("<option>", {
                                        'value': Number(themes_id),
                                        'html': themes_name
                                    });
                                    $('select[name=theme]').append(option);
                                }
                        }
                        else
                        {
                                    let option = $("<option>", {
                                        'value': 0,
                                        'html': "Aucun contenu disponible"
                                    });
                            $('select[name=theme]').append(option);
                        }


                    }
                }
            )
        });
 

  // Affiche dans la modal la liste des élèves du groupe sélectionné
        $('#level_id').on('change', function (event) {
            let id_level = $(this).val();
            let id_subject = $("#id_subject").val();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            $("#loading").html("<i class='fa fa-spinner fa-pulse fa-fw'></i>");
            $("#loading").show(); 
            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    traditional: true,
                    data: {
                        'id_level': id_level,
                        'id_subject': id_subject,                        
                        csrfmiddlewaretoken: csrf_token
                    },
                    url : "../ajax/chargethemes_parcours",
                    success: function (data) {

                        themes = data["themes"];
                        $('select[name=theme]').empty("");
                        if (themes.length >0)

                        { for (let i = 0; i < themes.length; i++) {
                                    

                                    console.log(themes[i]);
                                    let themes_id = themes[i][0];
                                    let themes_name =  themes[i][1]  ;
                                    let option = $("<option>", {
                                        'value': Number(themes_id),
                                        'html': themes_name
                                    });
                                    $('select[name=theme]').append(option);
                                }
                        }
                        else
                        {
                                    let option = $("<option>", {
                                        'value': 0,
                                        'html': "Aucun contenu disponible"
                                    });
                            $('select[name=theme]').append(option);
                        }


                        $('#parcours_details').html("").html(data.html);

                        $("#loading").hide(500); 
                    }
                }
            )
        });

        $('#thm_id').on('change', function (event) { 
 
            if (  $('select[name=level]').val() > 0 )
            {
                    let level_id = $('#level_id').val();
                    let theme_id = $(this).val();
                    let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
                    $("#loader").html("<i class='fa fa-spinner fa-pulse fa-3x fa-fw'></i>");
                                
                    $.ajax(
                        {
                            type: "POST",
                            dataType: "json",
                            traditional: true,
                            data: {
                                'level_id': level_id,
                                'theme_id': theme_id,
                                csrfmiddlewaretoken: csrf_token
                            },
                            url: '../ajax_all_parcourses',
                            success: function (data) {
         
                                $('#parcours_details').html("").html(data.html);
                                $("#loader").html("").hide(); 
                                
                                }
                        }
                    )
          
            }
            else 
            {   
                alert("Vous devez choisir un niveau."); return false;             
            }
        }); 





        $('#id_theme').on('change', function (event) {

            if (  $('select[name=level]').val() > 0 )
            {
                ajax_choice($('select[name=level]'),$('select[name=theme]')) ;            
            }
            else 
            {   
                alert("Vous devez choisir un niveau."); return false;             
            }
        }); 

        $('.send_message').on('click', function () {

            let name = $(this).attr("data-student_name"); 
            let email = $(this).attr("data-student_email"); 
 
            $('#email').val(email);
            $('#name').val(name);
 
            });


        function ajax_choice(param0, param1){

            let is_parcours = $("#is_parcours").val();
            let level_id = param0.val();
            let theme_id = param1.val();

            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            if ( is_parcours == "1" ) 
                { 
                    url= "../../ajax_level_exercise" ; 
                } 
            else 
                { 
                    url = "ajax_level_exercise";
                }

            var parcours_id = $("#id_parcours").val();

            $("#loader").html("<i class='fa fa-spinner fa-pulse fa-3x fa-fw'></i>");
                        

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    traditional: true,
                    data: {
                        'parcours_id': parcours_id ,
                        'level_id': level_id,
                        'theme_id': theme_id,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: url,
                    success: function (data) {
 
                        $('#content_exercises').html("").html(data.html);
                        $("#loader").html("").hide(); 
                        
                        }
                }
            )

        }

        $(".select_all").click(function(){
            value = $(this).val(); 
            $('#demo'+value+' .selector').not(this).prop('checked', this.checked);
        });


        $(".select_all_sg").click(function(){
            value = $(this).val(); 
            $('#demosg'+value+' .selector').not(this).prop('checked', this.checked);
        });



        $(".collapser").click(function(){
            value =  $(this).attr("data-group"); 
            $('.collapside'+value).toggle(500);
        });
        
        // Affiche div_results dans le parcours_show_student des élèves
        $('.div_results').hide();
        $('.div_results_custom').hide();

        $(".selector_div_result_custom").click(function(){
            value =  $(this).attr("data-customexercise_id"); 
            $('#div_results_custom'+value).toggle(500);
        });

        $(".div_results_custom_close").click(function(){
            value =  $(this).attr("data-customexercise_id"); 
            $('#div_results_custom'+value).toggle(500);
        });



        $(".selector_div_result").click(function(){
            value =  $(this).attr("data-relation_id"); 
            $('#div_results'+value).toggle(500);
        });

        $(".div_results_close").click(function(){
            value =  $(this).attr("data-relation_id"); 
            $('#div_results'+value).toggle(500);
        });


        // Affiche dans la modal la liste des élèves du groupe sélectionné
        $('.menuactionparcours').on('click', function (event) {
            let parcours_id = $(this).attr("data-parcours_id");
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            let is_disabled = $(this).attr("data-is_disabled");

            console.log(is_disabled) ;

            if (is_disabled == "0"){ $('#remove_student').prop('disabled', false); } else { $('#remove_student').prop('disabled', true) ; }

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'parcours_id': parcours_id,
                        csrfmiddlewaretoken: csrf_token,
                    },
                    url: "../../../group/ajax/chargelistgroup",
                    success: function (data) {
                        $('#parcours_id').val(parcours_id);
                        $('#modal_group_name').html(data.html_modal_group_name);
                        $('#list_students').html(data.html_list_students);
                    }
                }
            )
        });


        // Met en favori un parcours
        $('.selector_favorite').on('click' ,function () {
            let parcours_id = $(this).attr("data-parcours_id"); 
            let statut = $(this).attr("data-fav"); 
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'parcours_id': parcours_id,
                        'statut': statut,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "ajax_is_favorite",
                    success: function (data) {
                        $('#is_favorite_id'+parcours_id).html(data.statut);
                        $('#selector_favorite'+parcours_id).attr("data-fav",data.fav);      
                    }
                }
            )
        });



        // Affiche dans la modal la liste des élèves du groupe sélectionné
        $('.selector_e').on('click' ,function () {

            let parcours_id = $(this).attr("data-parcours_id"); 
            let exercise_id = $(this).attr("data-exercise_id"); 
            let statut = $(this).attr("data-statut"); 

            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'parcours_id': parcours_id,
                        'exercise_id': exercise_id,
                        'statut': statut,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "../../ajax_populate",
                    success: function (data) {
                        $('#is_selected'+exercise_id).html(data.html);   
                        $('#selector_e'+exercise_id).attr("data-statut",data.statut);                  
                        $('#selector_e'+exercise_id).removeClass(data.noclass);
                        $('#selector_e'+exercise_id).addClass(data.class);
                        if (data.no_store) { alert("Vous ne pouvez pas enregistrer cet exercice. Un exercice similaire est déjà dans ce parcours.")}
                    }
                }
            )
        });



        // Affiche dans la modal la liste des élèves du groupe sélectionné
        $('.select_student').on('click' , function () {

            let parcours_id = $(this).attr("data-parcours_id"); 
            let exercise_id = $(this).attr("data-exercise_id"); 
            let statut = $(this).attr("data-statut"); 
            let custom = $(this).attr("data-custom"); 
            let student_id = $(this).attr("data-student_id");
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            if (student_id != 0)
            {  
                if (statut == "True") {
                    if (!confirm('Vous souhaitez dissocier un élève à un exercice ?')) return false;                    
                }
            }
            else
            {    
                if (!confirm("Vous souhaitez modifier l'association de cet exercice à tout votre groupe ?")) return false;
            }


            if (custom == "1"){
                $("#loadingCustom"+exercise_id).html("<i class='fa fa-spinner fa-pulse fa-3x fa-fw'></i>"); 
            } else {
                $("#loading"+exercise_id).html("<i class='fa fa-spinner fa-pulse fa-3x fa-fw'></i>"); 
            }



            $.ajax( 
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'parcours_id': parcours_id,
                        'exercise_id': exercise_id,
                        'student_id': student_id,
                        'statut': statut,
                        'custom': custom,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "../../ajax_individualise",
                    success: function (data) {

                        if (custom == "1"){

                            if (student_id != 0)
                                {       
                                $('#studentCustom'+exercise_id+"-"+student_id).html(data.html);   
                                $('#studentCustom'+exercise_id+"-"+student_id).attr("data-statut",data.statut);                  
                                $('#studentCustom'+exercise_id+"-"+student_id).removeClass(data.noclass);
                                $('#studentCustom'+exercise_id+"-"+student_id).addClass(data.class);
                                }
                            else 
                                { 
                                $('.selected_studentCustom'+exercise_id).html(data.html);   
                                $('.selected_studentCustom'+exercise_id).attr("data-statut",data.statut);                  
                                $('.selected_studentCustom'+exercise_id).removeClass(data.noclass);
                                $('.selected_studentCustom'+exercise_id).addClass(data.class);                        
                                }

                            $("#loadingCustom"+exercise_id).html("");  
                            $('#selecteurCustom'+exercise_id).attr("data-statut",data.statut);   

                        }
                        else{ 

                            if (student_id != 0)
                                {       
                                $('#student'+exercise_id+"-"+student_id).html(data.html);   
                                $('#student'+exercise_id+"-"+student_id).attr("data-statut",data.statut);                  
                                $('#student'+exercise_id+"-"+student_id).removeClass(data.noclass);
                                $('#student'+exercise_id+"-"+student_id).addClass(data.class);
                                }
                            else 
                                { 
                                $('.selected_student'+exercise_id).html(data.html);   
                                $('.selected_student'+exercise_id).attr("data-statut",data.statut);                  
                                $('.selected_student'+exercise_id).removeClass(data.noclass);
                                $('.selected_student'+exercise_id).addClass(data.class);                      
                                }

     

                            $("#loading"+exercise_id).html("");  
                            $('#selecteur'+exercise_id).attr("data-statut",data.statut);    

                            }

                        if (data.alert){ alert("Certains exercices ont fait l'objet d'une réponse par certains élèves. Vous ne pouvez plus les dissocier.");}


                    }
                }
            )
        });



        $("#details_evaluation").hide();
             function makeItemAppearDetails($toggle, $item) {
                $toggle.change(function () {
                    if ($toggle.is(":checked")) {
                        $item.show(500);
                        $("#explain_evaluation").hide(500);
                    } else {
                        $item.hide(500);
                        $("#explain_evaluation").show(500);
                    }
                });
            }
            makeItemAppearDetails($("#id_is_evaluation"), $("#details_evaluation"));
 

        $(".overlay").hide();
        $(".overlay_show").click(function(){
            value =  $(this).attr("data-parcours_id"); 
            $('.overlay_show'+value).toggle(500);
        });



        $(".group_show").hide();
        $(".group_shower").click(function(){
            value =  $(this).attr("data-parcours_id"); 
            $('.group_show'+value).toggle(500);
        });

        $(".export_shower").click(function(){
            value =  $(this).attr("data-parcours_id"); 
            $('.overlay_export'+value).toggle(500);
        });

        // Affiche dans la modal la liste des élèves du groupe sélectionné
        $('.exportation_de_note').on('click' ,function () {

            let parcours_id = $(this).attr("data-parcours_id"); 
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            let value = $("#on_mark"+parcours_id).val(); 
            if(value=="") {alert("Vous devez renseigner cette valeur"); 
                                $("#on_mark"+parcours_id).focus();
                                 return false;}
            $("#loading_export"+parcours_id).html("<i class='fa fa-spinner fa-pulse fa-fw'></i>");  
                                            
            $.ajax(
                {
                    success: function (data) {

                        $("#loading_export"+parcours_id).html("").hide(); 
                    }
                }
            )
        });




        // Pour un élève... Depuis son parcours
        $('.read_my_production').on('click', function (event) {

            let custom = $(this).attr("data-custom");
            let exercise_id = $(this).attr("data-exercise_id");
            let student_id = $(this).attr("data-student_id");

            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'exercise_id': exercise_id,
                        csrfmiddlewaretoken: csrf_token,
                        'custom': custom,
                        'student_id': student_id,
                    },
                    url: "../../ajax_read_my_production",
                    success: function (data) {
                        $('#my_production_paper').html(data.html);
                    }
                }
            )
        });



        // Affiche dans la modal la liste des élèves du groupe sélectionné
        $('.header_shower').on('click', function (event) {
            let relation_id = $(this).attr("data-relation_id");
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            let parcours_id = $(this).attr("data-parcours_id");
            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'relation_id': relation_id,
                        csrfmiddlewaretoken: csrf_token,
                        'parcours_id': parcours_id,
                    },
                    url: "../../ajax/course_viewer",
                    success: function (data) {
                        $('#courses_from_section').html(data.html);
                    }
                }
            )
        });




        function display_custom_exercise_modal($actionner,$target){
              
            $actionner.on('click', function (event) {
                let customexerciseship_id = $(this).attr("data-customexercise_id");
                $($target+customexerciseship_id).toggle();
                $($target+customexerciseship_id).focus();                  
            });

        } ;

        display_custom_exercise_modal($('.custom_action_task'),"#custom_task_detail");

        display_custom_exercise_modal($('.custom_select_publish'),"#custom_detail_pub");
        display_custom_exercise_modal($('.custom_select_details'),"#custom_details");
        display_custom_exercise_modal($('.custom_sharer'),"#custom_share");

        display_custom_exercise_modal($('.custom_select_task_close'),"#custom_detail_dateur");
        display_custom_exercise_modal($('.custom_select_publish_close'),"#custom_detail_pub");
        display_custom_exercise_modal($('.custom_select_details_close'),"#custom_details");
        display_custom_exercise_modal($('.custom_select_share_close'),"#custom_share");

           
            $('.custom_select_task').on('click', function (event) {
                let relationship_id = $(this).attr("data-relationship_id");
                $("#custom_detail_dateur"+relationship_id).toggle();
                $("#custom_detail_dateur"+relationship_id).focus();
            });


        // Affiche dans la modal la liste des élèves du groupe sélectionné
        $('.attribute_to_parcours').on('click', function (event) {

            let parcours_id = $(this).attr("data-parcours_id");
            let exercise_id = $(this).attr("data-exercise_id");            
            let custom = $(this).attr("data-custom");

            $("#change_parcours_exercise_id").val(exercise_id);
            $("#change_parcours_parcours_id").val(parcours_id);
            $("#change_parcours_custom").val(custom);
        });



        // Pour le form_parcours
 
        if( $("#id_is_leaf").is(":checked")) { $('#folder_div').show(); } else { $('#folder_div').hide(); }

        $("#id_is_leaf").on('change', function (event) {
            $('#folder_div').toggle(500);
        });


        if( $("#id_is_folder").is(":checked")) { $('#leaf_div').show(); } else { $('#leaf_div').hide(); }
        
        $("#id_is_folder").on('change', function (event) {
            $('#leaf_div').toggle(500);
        });


            $(".click_subparcours_show").on('click', function (event) {
                let parcours_id = $(this).attr("data-parcours_id");
                $("#subparcours_show"+parcours_id).toggle(500);

                if( $(this).find("i").hasClass("fa-folder") ) 

                    { $(this).find("i").removeClass("fa-folder").addClass("fa-folder-open");}

                else 

                    { $(this).find("i").removeClass("fa-folder-open").addClass("fa-folder");}




            });












    });
});