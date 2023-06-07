define(['jquery','bootstrap_popover', 'bootstrap','chart'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-group.js OK");





        $('.dropdown-submenu').on('mouseover', function () {
            $(this).parent().find(".no_button").css('color','#EEE');
        })


        $('.dropdown-submenu').on('mouseout', function () {
            $(this).parent().find(".no_button").css('color','#5d4391');
        })

        $('.dropdown-submenu').on('mouseover', function () {
            $(this).css('color','#EEE');
        })



        //$('[data-toggle="popover"]').popover();

        $('.selector_color').on('click', function () {

            let code = $(this).attr("data-code");  
            $('#selected_color').html("<i class='fa fa-square text-"+code+"'></i>");
            $('#id_color').val(code);
            });

 
            $('#id_assign').on('change', function (){  

                if ( $('#id_assign').prop('checked') == false) {  
                    if (!confirm('Vous souhaitez dissocier tous les exercices de ce groupe ? Vous pourrez les rajouter plus tard.')) return false;
                    }  

                });
 
   
        $('.send_message').on('click', function () {

            let name = $(this).attr("data-student_name"); 
            let email = $(this).attr("data-student_email"); 
            let student_id = $(this).attr("data-student_id"); 
 
            $('#email').val(email);
            $('#name').val(name);
            $('#student_id').val(student_id);
            });

   


        // Affiche dans la modal la liste des élèves du groupe sélectionné
        $('#sender_message').on('click', function (event) {
            let name = $("#name").val(); 
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            alert("Vous venez d'envoyer un message à "+name+". Pour le retrouver, consulter votre boite de messages." );
        
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
                    url: "ajax/chargelisting",
                    success: function (data) {
                        $('#modal_group_name').html(data.html_modal_group_name);
                        $('#list_students').html(data.html_list_students);
                    }
                }
            )
        });



        // Affiche dans la modal la liste des élèves du groupe sélectionné
        $('#table_o').on('click', '.student_select_to_school' , function (event) {
            let group_id = $(this).attr("data_group_id");
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            let student_id = $(this).attr("data_student_id");

             console.log("loulou") ;

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'group_id': group_id,
                        'student_id': student_id,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "../../ajax/student_select_to_school",
                    success: function (data) {
                        $('#tr'+student_id).remove();
                        $("#maTable > tbody:last").append(data.html);
                        $("#maTable > tbody:last > tr:last > td:last a").addClass('student_remove_from_school');  
                    }
                }
            )
        });



        // Affiche dans la modal la liste des élèves du groupe sélectionné
        $('#maTable').on('click', ".student_remove_from_school", function (event) {
            let group_id = $(this).attr("data_group_id");
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            let student_id = $(this).attr("data_student_id");

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'group_id': group_id,
                        'student_id': student_id,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "../../ajax/student_remove_from_school",
                    success: function (data) {
                        $('#tr_school'+student_id).remove();
                        $("#table_o > tbody:last").append(data.html);

                    }
                }
            )
        });


        $('.updateStudent').on('keyup', function (event) {
            let value = $(this).val();
            let student_id = $(this).attr("data-student_id");
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            let is_name = $(this).attr("data-is_name");

            if( value.search(/[;=/]/)>-1) { alert("Vous avez tapé un caractère interdit");}
            else 
            {
                $.ajax(
                    {
                        type: "POST",
                        dataType: "json",
                        data: {
                            'value' :  value, 
                            'student_id' :  student_id, 
                            'is_name' :  is_name, 
                            csrfmiddlewaretoken: csrf_token
                        },
                        url: "../../../account/update_student_by_ajax",
                        success: function (data) {
                            if (is_name == 0)
                            {$('#studentFirstName'+student_id).val(value);}
                            else if (is_name == 1)
                            {$('#studentLastName'+student_id).val(value);}
                            else if (is_name == 2)
                            {$('#studentEmail'+student_id).val(value);}
                            else 
                            {$('#studentUsername'+student_id).val(value);}

                        },
                         error: function(){
                            alert(" L'identifiant "+value+" est déjà utilisé. En choisir un autre.") ; 
                         }
                    }
                )
            }
        });

        $(document).on('click',"#test_students", function(){ 

            $('#div_start_the_set_up').append("<i class='fa fa-spinner fa-pulse fa-2x'></i> Chargement en cours.") ;

        })


        // Affiche dans la modal la liste des élèves du groupe sélectionné
        $('.marklegend').on('click', function (event) {
            let knowledge_id = $(this).attr("data-knowledge_id");
            let group_id = $(this).attr("data-group_id");
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
 
            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'knowledge_id' :  knowledge_id, 
                        'group_id' :  group_id, 
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "../../../ajax/select_exercise_by_knowledge",
                    success: function (data) {
                        $('#knowledge_id_modal').val(knowledge_id);
                        $('#select_exercises').html("").html(data.html);
                    }
                }
            )
        });


 

        $("#print_stats").on('click' ,function () {    
            $("#loading_stats").html("<i class='fa fa-spinner fa-pulse fa-fw'></i>"); 
            $.ajax({
              success: function(){
                    $("#loading_stats").html("").hide();
              }
            });
        });


        $(".recording").hide() ;

        $("#record_student_now").on('click' ,function () {    
            $("#teacher_record").show();
            $("#auto_record").hide();  
            $("#collapsed").hide();           
        });

        $("#record_student_auto").on('click' ,function () {    
            $("#teacher_record").hide();
            $("#auto_record").show(); 
            $("#collapsed").hide();          
        });

        $("#record_student_add").on('click' ,function () {    
            $("#teacher_record").hide();
            $("#auto_record").hide();
            $("#collapsed").show();            
        });


            $('.div_username').on('click', function (){  
 
                    let username_div = $(this).data("username_div");

                    $("#response_username").html(username_div) ;
                });




        $("#choose_parcours").hide() ;
        $("#choosen_parcours_for_this_level_and_subject").hide() ;

 
        $("#id_studentprofile").change(function () {

            if ($("#id_studentprofile").is(":checked")) {
                $("#choose_parcours").show(500);
                $("#choosen_parcours_for_this_level_and_subject").show(500);
                $("#choosen_parcours_by_this_level_and_subject").show(500);
            } else {
                $("#choose_parcours").hide(500);
                $("#choosen_parcours_for_this_level_and_subject").hide(500);
                $("#choosen_parcours_by_this_level_and_subject").hide(500);
            }

        });
  



        $('.add_homeworkless').on('click', function () {

            let student_id = $(this).data("student_id");
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
 
            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'student_id': student_id,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "../ajax_add_homeworkless/",
                     success: function (data) {                        
                        var nb = parseInt( $('#homeworkless'+student_id).html() ) + 1;
                        if (data.create == "yes")
                        { $('#homeworkless'+student_id).html(nb);}
                        else {
                            alert("Enregistrement déjà effectué pour ce jour")
                        }
                    }
                }
            )

            });



        $('.remove_homeworkless').on('click', function () {

            let h_id = $(this).data("h_id");
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            let student_id = $(this).data("student_id");
            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'h_id': h_id,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "../ajax_remove_homeworkless/",
                     success: function (data) {
                        var nb = parseInt( $('#homeworkless'+student_id).html() ) - 1;
                        $('#h_'+h_id).remove();
                        $('#homeworkless'+student_id).html(nb);
                    }
                }
            )

            });


        $('.add_toolless').on('click', function () {

            let student_id = $(this).data("student_id");
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
 
            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'student_id': student_id,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "../ajax_add_toolless/",
                     success: function (data) {
                        var nb = parseInt( $('#toolless'+student_id).html() ) + 1;
                        if (data.create == "yes")
                        { $('#toolless'+student_id).html(nb);}
                        else {
                            alert("Enregistrement déjà effectué pour ce jour")
                        }
                    }
                }
            )

            });


        $('.remove_toolless').on('click', function () {

            let t_id = $(this).data("t_id");
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            let student_id = $(this).data("student_id");
            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        't_id': t_id,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "../ajax_remove_toolless/",
                     success: function (data) {
                        var nb = parseInt( $('#toolless'+student_id).html() ) - 1;
                        $('#t_'+t_id).remove();
                        $('#toolless'+student_id).html(nb);
                    }
                }
            )

            });



        $('.remove_homeworkless_mini').on('click', function () {

            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            let student_id = $(this).data("student_id");
            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'student_id': student_id,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "../ajax_remove_homeworkless_mini/",
                     success: function (data) {
                        var nb = parseInt( $('#homeworkless'+student_id).html() ) - 1;
                        $('#toolless'+student_id).html(nb);
                    }
                }
            )
        });




        $('.remove_toolless_mini').on('click', function () {

            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            let student_id = $(this).data("student_id");
            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'student_id': student_id,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "../ajax_remove_toolless_mini/",
                     success: function (data) {
                        var nb = parseInt( $('#toolless'+student_id).html() ) - 1;
                        $('#toolless'+student_id).html(nb);
                    }
                }
            )
        });





       
    });
});