define(['jquery', 'bootstrap', 'ui', 'ui_sortable'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-dashboard.js OK");
        console.log("dashboard chargé celui-ci.");




  $(window).on('load', function () {
    if ($('#preloader').length) {
      $('#preloader').delay(100).fadeOut('slow', function () {
        $(this).remove();
      });
    }
  });

 

 
        $(".overlay").hide();
        $(".overdiv_show").click(function(){
            value =  $(this).attr("data-student_id"); 
            $('.overdiv_show'+value).toggle(500);
        });


        $('.content-wrapper').removeAttr("style");

        $('#account').click(function(event) {
          if ($('#notification-account').hasClass('dismiss')) {
            $('#notification-account').removeClass('dismiss').addClass('selected').show();
            $('#notification-admin').removeClass('selected').addClass('dismiss');
          }
          event.preventDefault();
        });

        $('#closeAccount').click(function(event) {
          if ($('#notification-account').hasClass('selected')) {
            $('#notification-account').removeClass('selected').addClass('dismiss');
          }
          event.preventDefault();
        });


        var pub = 0 ;

        $('#admin').click(function(event) { 
          if ( pub%2 == 0 ) {
              if ($('#notification-admin').hasClass('dismiss')) {
                $('#notification-admin').removeClass('dismiss').addClass('selected').show();
                $('#notification-account').removeClass('selected').addClass('dismiss');
              }

            }
            else
            {
              $('#notification-admin').removeClass('selected').addClass('dismiss');
            }
            event.preventDefault();        
            pub ++ ;
            console.log(pub) ; 
        });

        var show = 0 ;

        $('.detail_student').click(function(event) { 
          if ( show%2 == 0 ) 
            {
                $('#notification-perso').removeClass('dismissR').addClass('selectedR').show();

                let student_id =  $(this).attr("data-student_id");  
                let theme_id =  $(this).attr("data-theme_id"); 
                let group_id =  $(this).attr("data-group_id"); 
                let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
                $.ajax({
                    url: '../../../../account/ajax_detail_student/'  ,
                    data: {
                        'student_id': student_id,
                        'theme_id': theme_id,
                        'group_id': group_id,
                        csrfmiddlewaretoken: csrf_token,                        
                    },
                    type: "POST",
                    dataType: "json",
                    success: function (data) {

                        $("#detail_of_student").html("").html(data["html"]);
     
                        $('#closeStudent').click(function(event) {
                            show--;
                            if ($('#notification-perso').hasClass('selectedR')) 
                            {
                            $('#notification-perso').removeClass('selectedR').addClass('dismissR');
                            }
                            event.preventDefault();
                        });


                    }
                });
 

            }
            else
            {
                $('#notification-perso').removeClass('selectedR').addClass('dismissR');
            }
            event.preventDefault();        
            show ++ ;
        });


        var view = 0 ;
        $('.detail_student_exercise').click(function(event) {  
          if ( view%2 == 0 ) 
            {
                $('#notification-perso').removeClass('dismissR').addClass('selectedR').show();

                let student_id =  $(this).attr("data-student_id");  
                let parcours_id =  $(this).attr("data-parcours_id"); 
 
                let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

                $.ajax({
                    url: '../../../../account/ajax_detail_student_exercise/'  ,
                    data: {
                        'student_id': student_id,
                        'parcours_id': parcours_id,
                        csrfmiddlewaretoken: csrf_token,                        
                    },
                    type: "POST",
                    dataType: "json",
                    success: function (data) {

                        $("#detail_of_student").html("").html(data["html"]);
     
                        $('#closeStudent').click(function(event) {
                            view--;
                            if ($('#notification-perso').hasClass('selectedR')) 
                            {
                            $('#notification-perso').removeClass('selectedR').addClass('dismissR');
                            }
                            event.preventDefault();
                        });
                    }
                });
            }
            else
            {
                $('#notification-perso').removeClass('selectedR').addClass('dismissR');
            }
            event.preventDefault();        
            view ++ ;
        });



        $('.detail_parcours').click(function(event) { 
          if ( show%2 == 0 ) 
            {
                $('#notification-perso').removeClass('dismissR').addClass('selectedR').show();

                let exercise_id =  $(this).attr("data-exercise_id");  
                let parcours_id =  $(this).attr("data-parcours_id");  
                let num_exo =  $(this).attr("data-num_exo");  

                let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
                $.ajax({
                    url: '../../../../qcm/ajax_detail_parcours/'  ,
                    data: {
                        'exercise_id': exercise_id,
                        'parcours_id': parcours_id,
                        'num_exo': num_exo,

                        csrfmiddlewaretoken: csrf_token,                        
                    },
                    type: "POST",
                    dataType: "json",
                    success: function (data) {

                        $("#detail_of_student").html("").html(data["html"]);
     
                        $('#closeStudent').click(function(event) {
                            show--;
                            if ($('#notification-perso').hasClass('selectedR')) 
                            {
                            $('#notification-perso').removeClass('selectedR').addClass('dismissR');
                            }
                            event.preventDefault();
                        });


                    }
                });
 

            }
            else
            {
                $('#notification-perso').removeClass('selectedR').addClass('dismissR');
            }
            event.preventDefault();        
            show ++ ;
        });

        // ====================================================================================================================
        // ====================================================================================================================
        // =================================   Toggle sur la div des élèves d'un groupe ======================================= 
        // ====================================================================================================================
        // ====================================================================================================================

        $('#handler_order_exercises').click(function(event) {  
          if ( show%2 == 0 ) 
            {
                $('#order_exercises').removeClass('dismissR').addClass('selectedR').show();
            }
            else
            {
                $('#order_exercises').removeClass('selectedR').addClass('dismissR');
            }
            event.preventDefault();        
            show ++ ;
        });

        // ====================================================================================================================
        // ====================================================================================================================
        // =================================   Toggle sur la div des élèves d'un groupe ======================================= 
        // ====================================================================================================================
        // ====================================================================================================================

        $('.detail_student_parcours').click(function(event) { 
          if ( show%2 == 0 ) 
            {
                $('#notification-perso').removeClass('dismissR').addClass('selectedR').show();

                let student_id =  $(this).attr("data-student_id");  
                let parcours_id =  $(this).attr("data-parcours_id"); 
                let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
                $.ajax({
                    url: '../../../../account/ajax_detail_student_parcours/'  ,
                    data: {
                        'student_id': student_id,
                        'parcours_id': parcours_id,
                        csrfmiddlewaretoken: csrf_token,                        
                    },
                    type: "POST",
                    dataType: "json",
                    success: function (data) {

                        $("#detail_of_student").html("").html(data["html"]);
     
                        $('#closeStudent').click(function(event) {
                            show--;
                            if ($('#notification-perso').hasClass('selectedR')) 
                            {
                            $('#notification-perso').removeClass('selectedR').addClass('dismissR');
                            }
                            event.preventDefault();
                        });


                    }
                });
 

            }
            else
            {
                $('#notification-perso').removeClass('selectedR').addClass('dismissR');
            }
            event.preventDefault();        
            show ++ ;
        });

        // ====================================================================================================================
        // ====================================================================================================================
        // =================================   Toggle sur la div des élèves d'un groupe ======================================= 
        // ====================================================================================================================
        // ====================================================================================================================
        $("#parcours_div").hide();
        $("#select_parcours_div").click(function(){
            $('#parcours_div').toggle(500);
        });




        // ====================================================================================================================
        // ====================================================================================================================
        // =================================   Toggle sur la div des élèves d'un groupe ======================================= 
        // ====================================================================================================================
        // ====================================================================================================================
        $(".group_show").hide();
        $(".group_shower").click(function(){
            value =  $(this).attr("data-group_id"); 
            $('.group_show'+value).toggle(500);
        });


        // Affiche dans la modal la liste des élèves du groupe sélectionné
        $('.menuaction').on('click', function (event) {
            let group_id = $(this).attr("data-group_id");
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
 
            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'group_id': group_id,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "group/ajax/chargelisting",
                    success: function (data) {
                        $('#modal_group_name').html(data.html_modal_group_name);
                        $('#list_students').html(data.html_list_students);
                    }
                }
            )
        });



        // ====================================================================================================================
        // ====================================================================================================================
        // ============================================    Fermeture du volet admin    ========================================= 
        // ====================================================================================================================
        // ====================================================================================================================





        $('#closeAdmin').click(function(event) {
          if ($('#notification-admin').hasClass('selected')) {
            $('#notification-admin').removeClass('selected').addClass('dismiss');
          }
          event.preventDefault();
        });

        // ====================================================================================================================
        // ====================================================================================================================
        // ============================================    Recherhe d'un exercice     ========================================= 
        // ====================================================================================================================
        // ====================================================================================================================

        $('#search').on('keyup', function () {


            let search =  $(this).val()  ;   
            let from =  $("#from").val()  ;             
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            if (from) { urlform = '../../qcm/ajax_search_exercise' ;}   else { urlform = 'qcm/ajax_search_exercise' ;} 
          
            if (search.length > 5)

            { 
                $.ajax({
                    url: urlform ,
                    data: {
                        'search': search,
                        csrfmiddlewaretoken: csrf_token,                        
                    },
                    type: "POST",
                    dataType: "json",
                    success: function (data) {

                        $("#search_result").html("").html(data["html"]);
     
                    }
                });
            }

        });


        // ====================================================================================================================
        // ====================================================================================================================
        // ============================================    Rejoindre un  cours     ============================================ 
        // ====================================================================================================================
        // ====================================================================================================================


        $('#aggregate_form').hide();  
        $('#aggregate_groupe').click(function(event) {
                 $('#aggregate_form').toggle(500);  
            });


        $('#id_groupe').on('keyup', function () {
             
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();        
            let groupe_code =  $(this).val()  ;

            $.ajax({
                type: "POST",
                dataType: "json",
                url: '../account/ajax/courseinfo/',
                data: {
                    'groupe_code': groupe_code,
                    csrfmiddlewaretoken: csrf_token,                        
                },
                success: function (data) {

                    $(".verif_course").html(data["htmlg"]); 
                     $('#registerstudent').prop("disabled", false);
                }
            });
        });


        $('#aggregate_parcours_form').hide();  
        $('#aggregate_parcours').click(function(event) {
                 $('#aggregate_parcours_form').toggle(500);  
            });


        $('#id_parcours').on('keyup', function () {
             
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
          

            let code =  $(this).val()  ;

            $.ajax({
                url: '../qcm/ajax_parcoursinfo/',
                data: {
                    'code': code,
                    csrfmiddlewaretoken: csrf_token,                        
                },
                type: "POST",
                dataType: "json",
                success: function (data) {

                    $(".verif_parcours").html(data["htmlg"]);
 
                }
            });
        }); 

        // ====================================================================================================================
        // ====================================================================================================================
        // ============================================  Organisation du parcours  ============================================ 
        // ====================================================================================================================
        // ====================================================================================================================
        $('#closeOrganiser').click(function(event) {
          if ($('#order_exercises').hasClass('selectedR')) {
            $('#order_exercises').removeClass('selectedR').addClass('dismissR');
          }
          event.preventDefault();
        });
 

         $('#exercise_sortable_list').sortable({
            cursor: "move",   
            distance: 10,
            revert: true,
            start: function( event, ui ) { 
                   $(ui.item).css("box-shadow", "10px 5px 10px gray").css("background-color", "#271942").css("color", "#FFF"); 
               },
            stop: function (event, ui) {


                let parcours = $("#parcours").val();
                var valeurs = "";
                         
                $(".sorted_exercise_id").each(function() {
                    let this_exercise_id = $(this).val();
                    valeurs = valeurs + this_exercise_id +"-";
                });

                $(ui.item).css("box-shadow", "0px 0px 0px transparent").css("background-color", "#dbcdf7").css("color", "#271942"); 

                $.ajax({
                        data:   { 'valeurs': valeurs , 'parcours' : parcours,  } ,   
                        type: "POST",
                        dataType: "json",
                        url: "../../ajax/sort_exercise" 
                    }); 
                }
            });

 
     
     
        $('.exercise_sortable').sortable({
            cursor: "move",
            swap: true,    
            animation: 150,
            distance: 10,
            revert: true,
            tolerance: "pointer" , 
            start: function( event, ui ) { 
                   $(ui.item).css("box-shadow", "10px 5px 10px gray"); 
               },
            stop: function (event, ui) {


                let parcours = $("#parcours").val();
                var valeurs = "";
                         
                $(".div_exercise_id").each(function() {
                    let div_exercise_id = $(this).val();
                    valeurs = valeurs + div_exercise_id +"-";
                });
                $(ui.item).css("box-shadow", "0px 0px 0px transparent");  

                $.ajax({
                        data:   { 'valeurs': valeurs , 'parcours' : parcours,  } ,   
                        type: "POST",
                        dataType: "json",
                        url: "../../ajax/sort_exercise" 
                    }); 
                }
            });
 


        $('#create_section').click(function(event) {   

            let value = $('#section_fill').val();  
            let subtitle = $('#subtitle').val(); 
            let parcours_id = $('#parcours_id').val(); 
            if (subtitle=="1") { subtitle = 1;} else { subtitle = 0;}

            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            $.ajax({
                url: '../../ajax/create_title_parcours',
                data: {
                    'value': value,
                    'subtitle': subtitle,
                    'parcours_id': parcours_id,

                    csrfmiddlewaretoken: csrf_token,                        
                },
                type: "POST",
                dataType: "json",
                success: function (data) {
                $(data.html).insertBefore( $('#miseEnAttenteDashboard').children()[0] );
                }
            });
        });


        $('body').on('click','.erase_title', function (){   
            let parcours_id = $(this).attr('data-parcours_id');  
            let exercise_id = $(this).attr('data-exercise_id');  
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            if (!confirm('Vous souhaitez supprimer cette section/sous-section ?')) return false;

            $.ajax({
                url: '../../ajax/erase_title',
                data: {
                    'parcours_id': parcours_id,
                    'exercise_id': exercise_id,
                    csrfmiddlewaretoken: csrf_token,                        
                },
                type: "POST",
                dataType: "json",
                success: function (data) { 
                $("#new_title"+exercise_id).remove() ;
                }
            });
        });



        // ==================================================================================================================  
        // ==================================================================================================================             
        // ============================================   Date limite des tasks  ============================================ 
        // ================================================================================================================== 
        // =================================================================================================================

 
 
            $('#form_error_set').hide();  
            $('#error_set').click(function(event) {
                     $('#form_error_set').toggle(500);  
                });


        $('#error_sender').on('click', function () {
             
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
          
            let message =  $("#message").val()  ;
            let exercise_id =  $(this).attr("data-exercise_id");   
            let from =  $(this).attr("data-from");   

            if (from == "0") { url_to ="../../ajax/exercise_error"} else  { url_to ="../ajax/exercise_error" ; } 
 
            $.ajax({
                url: url_to,
                data: {
                    'message': message,
                    'exercise_id': exercise_id,
                    csrfmiddlewaretoken: csrf_token,                        
                },
                type: "POST",
                dataType: "json",
                success: function (data) {

                    $(".verif_sender").html(data.htmlg);
 
                }
            });
        });





            $("#task_date").hide(500);
            $("#publish_date").hide(500);

            function makeItemAppear($toggle, $item) {
                    $toggle.change(function () {
                        if ($toggle.is(":checked")) {
                            $item.show(500);
                        } else {
                            $item.hide(500);
                        }
                    });
                }

            function makeItemDisappear($toggle, $item) {
                    $toggle.change(function () {
                        if ($toggle.is(":checked")) {
                            $item.hide(500);
                        } else {
                            $item.show(500);
                        }
                    });
                }
            makeItemAppear($("#id_is_task"), $("#task_date"));
            makeItemDisappear($("#id_is_publish"), $("#publish_date"));



 




            // Affiche dans la modal la liste des élèves du groupe sélectionné
            $('.select_group').on('click', function (event) {
                let group_id = $(this).attr("data-group_id");
                let group_name = $(this).attr("data-group_name");
                let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
                let from = $(this).attr("data-from");
                if (from == "0") { url_to ="../../../ajax/chargelisting"} else  { url_to ="../../ajax/chargelisting" ; } 
     
                $.ajax(
                    {
                        type: "POST",
                        dataType: "json",
                        data: {
                            'group_id': group_id,
                            'group_name': group_name,
                            csrfmiddlewaretoken: csrf_token
                        },
                        url: url_to ,
                        success: function (data) {
                            $('#modal_group_name').html(group_name);
                            $('#list_students').html(data.html_list_students);
                        }
                    }
                )
                });

                 // Publie ou dépublie un exercice
            $('.action_content').on('click', function (event) {
                let relationship_id = $(this).attr("data-relationship_id");
                let statut = $(this).attr("data-statut");
                let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

                $.ajax(
                    {
                        type: "POST",
                        dataType: "json",
                        data: {
                            'relationship_id': relationship_id,
                            'statut': statut,
                            csrfmiddlewaretoken: csrf_token
                        },
                        url: "../../ajax/publish" ,
                        success: function (data) {
                            $('#starter'+relationship_id).toggle();
                            $('#publisher'+relationship_id).attr("data-statut",data.statut);                  
                            $('#publisher'+relationship_id).html("").html(data.publish);
                            $('#publisher'+relationship_id).removeClass(data.noclass);
                            $('#publisher'+relationship_id).addClass(data.class);
                        }
                    }
                )
                });   

        // ==================================================================================================
        // ==================================================================================================
        // ============= Publication de parcours
        // ==================================================================================================
        // ==================================================================================================

            function publisher_parcours($actionner,$target,$targetStatut){


  
                $actionner.on('click', function (event) {
                let parcours_id = $(this).attr("data-parcours_id");
                let statut = $(this).attr("data-statut");
                let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
                let from = $(this).attr("data-from");



                if( from == "2")  { url_from = "../../ajax/publish_parcours" ; } 
                else if (from == "0") {  url_from = "../../../ajax/publish_parcours" ;} 
                else  { url_from = "ajax/publish_parcours" ;} 

 
                $.ajax(
                    {
                        type: "POST",
                        dataType: "json",
                        data: {
                            'parcours_id': parcours_id,
                            'statut': statut,
                            'from': from,
                            csrfmiddlewaretoken: csrf_token
                        },
                        url: url_from ,
                        success: function (data) {
                            $($target+parcours_id).attr("data-statut",data.statut);                  
                            $($targetStatut+parcours_id).removeClass(data.noclass);
                            $($targetStatut+parcours_id).addClass(data.class);
                            $($targetStatut+parcours_id).html("").html(data.label);

                            if( from =="2") { 
                            $('.disc'+parcours_id).css("background-color",data.style); 
                            }  
                        }
                    }
                )

                }); 
            } ;

            publisher_parcours( $('.publisher') , '#parcours_publisher' ,'#parcours_statut' ) ;
 

 

/*
            // Publie ou dépublie un parcours à partir de la liste des parcours
            $('.publisher').on('click', function (event) {
                let parcours_id = $(this).attr("data-parcours_id");
                let statut = $(this).attr("data-statut");
                let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
                let from = $(this).attr("data-from");

                if( from ==2) { url_from = "../../ajax/publish_parcours" ; } else {url_from = "ajax/publish_parcours" ; }
                $.ajax(
                    {
                        type: "POST",
                        dataType: "json",
                        data: {
                            'parcours_id': parcours_id,
                            'statut': statut,
                            'from': from,
                            csrfmiddlewaretoken: csrf_token
                        },
                        url: url_from ,
                        success: function (data) {
                            $('#parcours_publisher'+parcours_id).attr("data-statut",data.statut);                  
                            $('#parcours_publisher'+parcours_id).html("").html(data.publish);
                            $('#parcours_publisher'+parcours_id).removeClass(data.noclass);
                            $('#parcours_publisher'+parcours_id).addClass(data.class);
                            if( from ==2) { 
                            $('.disc'+parcours_id).css("background-color",data.style); 
                            }                         
                        }
                    }
                )
                }); 


            // Publie ou dépublie un parcours à partir du sous menu barre haute des parcours  Bouton double
            $('#parcours_publisher').on('click', function (event) {
                let parcours_id = $(this).attr("data-parcours_id");
                let statut = $(this).attr("data-statut");
                let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
                let from = $(this).attr("data-from");
                if (from == 0) {  url_from = "../../../ajax/publish_parcours" ;} else { url_from = "../../ajax/publish_parcours" ;} 

                $.ajax(
                    {
                        type: "POST",
                        dataType: "json",
                        data: {
                            'parcours_id': parcours_id,
                            'statut': statut,
                            'from': from,
                            csrfmiddlewaretoken: csrf_token
                        },
                        url: url_from ,
                        success: function (data) {
                            $('#parcours_publisher').attr("data-statut",data.statut);                  
                            $('#parcours_publisher').html("").html(data.publish);
                            $('#parcours_statut').removeClass(data.noclass);
                            $('#parcours_statut').addClass(data.class);
                            $('#parcours_statut').html("").html(data.label);

                        }
                    }
                )
                });  

*/
        // ==================================================================================================
        // ==================================================================================================
        // ============= Affiche une fenetre modale personnalisée
        // ==================================================================================================
        // ==================================================================================================
            $(".card-dateur").hide();
            $(".card-skill").hide();

            function display_custom_modal($actionner,$target){
  

                $actionner.on('click', function (event) {
                    let relationship_id = $(this).attr("data-relationship_id");
                    $($target+relationship_id).toggle();
                    $($target+relationship_id).focus();
                });

            } ;

            display_custom_modal($('.action_task'),"#task_detail");
            display_custom_modal($('.select_task'),"#detail_dateur");
            display_custom_modal($('.select_publish'),"#detail_pub");
            display_custom_modal($('.select_details'),"#details");
            display_custom_modal($('.sharer'),"#share");
            display_custom_modal($('.select_skills'),"#skill");

  
            display_custom_modal($('.select_task_close'),"#detail_dateur");
            display_custom_modal($('.select_publish_close'),"#detail_pub");
            display_custom_modal($('.select_details_close'),"#details");
            display_custom_modal($('.select_share_close'),"#share");
            display_custom_modal($('.select_skill_close'),"#skill");


        // ==================================================================================================
        // ==================================================================================================
        // =============  FIN des modales
        // ==================================================================================================
        // ==================================================================================================


            $('.skill_selector').on('click', function (event) {
                let relationship_id = $(this).attr("data-relationship_id");
                let skill_id = $(this).val();

                console.log(relationship_id);
                console.log(skill_id);

                let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
                $.ajax(
                    {
                        type: "POST",
                        dataType: "json",
                        data: {
                            'relationship_id': relationship_id,
                            'skill_id': skill_id,
                            csrfmiddlewaretoken: csrf_token
                        },
                        url: "../../ajax/skills" ,
                    }
                )

                });    


            $(".copy").on("click", function() {

                let parcours_id = $(this).attr("data-parcours_id");
                let exercise_id = $(this).attr("data-exercise_id");  
                let relationship_id = $(this).attr("data-relationship_id");  
 
                  if (!confirm("Pour coller dans une page, sélectionner et copier (CTRL+C) :                    http://parcours.erlm.tn/qcm/"+parcours_id+"/"+exercise_id+"/")) return false;
                    $("#share"+relationship_id).toggle();


                }

                );


            $('.dates').on('change', function (event) {
                let relationship_id = $(this).attr("data-relationship_id");
                let type = $(this).attr("data-type");
                let dateur = $(this).val();
                let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
                $("#loading"+relationship_id).html("<i class='fa fa-spinner fa-pulse fa-fw'></i>");  
 
                $.ajax(
                    {
                        type: "POST",
                        dataType: "json",
                        data: {
                            'relationship_id': relationship_id,
                            'dateur': dateur,
                            'type': type,
                            csrfmiddlewaretoken: csrf_token
                        },
                        url: "../../ajax/dates" ,
                        success: function (data) {
                            $("#loading"+relationship_id).html("");  
                            if (type == 0)
                                { $('#starter'+relationship_id).val(data.dateur); $('#starter'+relationship_id).val(data.dateur);}
                            else
                                { $('#dateur'+relationship_id).val(data.dateur);
                                $('#pub_task'+relationship_id).html('').html(data.label); }              

                        }
                    }
                )

                });


            $('.dateur').on('change', function (event) {
                let relationship_id = $(this).attr("data-relationship_id");
                let type = $(this).attr("data-type");
                let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

                console.log(type,  relationship_id) ; 
                $("#loading"+relationship_id).html("<i class='fa fa-spinner fa-pulse fa-fw'></i>"); 
                
                let dateur = $(this).val();
                    datas = {
                            'relationship_id': relationship_id,
                            'dateur': dateur,
                            'type': type,
                            csrfmiddlewaretoken: csrf_token
                        } ;

                $.ajax(
                        {
                            type: "POST",
                            dataType: "json",
                            data: datas,
                            url: "../../ajax/dates" ,
                            success: function (data) {
                            $("#loading"+relationship_id).html("");  
                                if (type == 0)
                                    { $('#starter'+relationship_id).val(data.dateur); 
                                    $("#detail_pub"+relationship_id).hide();
                                    }
 

                                else 
                                    { $('#dateur'+relationship_id).val(data.dateur);
                                    $('#pub_task'+relationship_id).html('').html(data.dateur); 
                                    $('#pub_task'+relationship_id).addClass(data.class);
                                    $('#pub_task'+relationship_id).removeClass(data.noclass); 
                                    $("#detail_dateur"+relationship_id).hide();
                                } 

                            }
                        }
                    )
                    .done(function() {
                          $( this ).focus();
                        });

                });


            $('.details_relation').on('keyup', function (event) {
                let relationship_id = $(this).attr("data-relationship_id");
                let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
                let situation = $("#situation"+relationship_id).val();

                let duration = $("#duration"+relationship_id).val();
                let type = $(this).attr("data-type");

                console.log(situation, duration,  relationship_id) ; 

                datas = {   'relationship_id': relationship_id,
                            'situation': situation,
                            'duration' : duration,
                            'type' : type,
                            csrfmiddlewaretoken: csrf_token,
                        } ;
                $.ajax(
                    {
                        type: "POST",
                        dataType: "json",
                        data: datas,
                        url: "../../ajax/dates" ,
                        success: function (data) {
                            console.log(data);
                            if (data.clock) {
                                $('#clock'+relationship_id).html("").html(data.clock); 
                                $('#duration'+relationship_id).val(duration);                                 
                            }
                            if (data.save) {
                                $('#save'+relationship_id).html("").html(data.save);
                                $('#situation'+relationship_id).val(situation);
                            }


                        }
                    }
                )
                });

        // ==================================================================================================================  
        // ==================================================================================================================             
        // ====================================================   Flex page  === ============================================ 
        // ================================================================================================================== 
        // ==================================================================================================================  


            var flex_size = 0;
            $('#buttonToggle').on('click', function () {

                        if ( flex_size%2 == 0)
                            {
                            $('#sub_menu_left').css("display","none")
                            $('#flex').attr("class","col-xs-12 col-md-12")
                            if ($('#sub_menu_left')) 
                                {$('#inside_flex').css("padding","20px") ;}

                            $('#buttonToggle').css("color","orange") ;

                            }
                        else
                           {
                            $('#sub_menu_left').css("display","block")
                            $('#flex').attr("class","col-xs-12 col-md-10")
                            if ($('#sub_menu_left')) 
                                {$('#inside_flex').css("padding","0px") ;}

                            $('#buttonToggle').css("color","#309ae4") ;
                            } 
                            flex_size ++;
                        });

        // ==================================================================================================================  
        // ==================================================================================================================             
        // ====================================================   fenetre modale ============================================ 
        // ================================================================================================================== 
        // ==================================================================================================================  
 
            $('.remediation').on('click', function (event) {
                let relationship_id = $(this).attr("data-relationship_id");
                let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
                console.log(relationship_id);
                $.ajax(
                    {
                        type: "POST",
                        dataType: "json",
                        data: {
                            'relationship_id': relationship_id,
                            csrfmiddlewaretoken: csrf_token
                        },
                        url: "../../ajax/remediation" ,
                        success: function (data) {
                            $('#remediation_form').html('').html(data.html);          
                        }
                    }
                )

                });


 
            $('.remediation_viewer').on('click', function (event) {
                let remediation_id = $(this).attr("data-remediation_id");
                let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
                console.log(remediation_id);
                $("#loader_shower").html("<i class='fa fa-spinner fa-pulse fa-fw fa-3x'></i>");  
                $.ajax(
                    {
                        type: "POST",
                        dataType: "json",
                        data: {
                            'remediation_id': remediation_id,
                            csrfmiddlewaretoken: csrf_token
                        },
                        url: "../../ajax/remediation_viewer" ,
                        success: function (data) {
                            $('#remediation_shower').html('').html(data.html);          
                        }
                    }
                )

                });



    });        
});