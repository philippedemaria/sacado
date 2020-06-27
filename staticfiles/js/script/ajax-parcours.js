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
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            console.log(id_level) ; 
 
            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    traditional: true,
                    data: {
                        'id_level': id_level,
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




 
        $('select[name=theme]').on('change', function (event) {

            if ($('select[name=level]').val())
            {
                ajax_choice($('select[name=level]'),$('select[name=theme]')) ;
            }
            else 
            {   alert("Vous devez choisir un niveau."); return false;}
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



        $(".collapser").click(function(){
            value =  $(this).attr("data-group"); 
            $('.collapside'+value).toggle(500);
        });
        


        // Affiche dans la modal la liste des élèves du groupe sélectionné
        $('.menuactionparcours').on('click', function (event) {
            let parcours_id = $(this).attr("data-parcours_id");
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
 
            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'parcours_id': parcours_id,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "../../../group/ajax/chargelistgroup",
                    success: function (data) {
                        $('#modal_group_name').html(data.html_modal_group_name);
                        $('#list_students').html(data.html_list_students);
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

                    }
                }
            )
        });



        // Affiche dans la modal la liste des élèves du groupe sélectionné
        $('.select_student').on('click' ,function () {

            let parcours_id = $(this).attr("data-parcours_id"); 
            let exercise_id = $(this).attr("data-exercise_id"); 
            let statut = $(this).attr("data-statut"); 
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



            $("#loading"+exercise_id).html("<i class='fa fa-spinner fa-pulse fa-3x fa-fw'></i>"); 
            $.ajax( 
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'parcours_id': parcours_id,
                        'exercise_id': exercise_id,
                        'student_id': student_id,
                        'statut': statut,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "../../ajax_individualise",
                    success: function (data) {

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


    });
});