define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-group.js OK");


        $('[data-toggle="popover"]').popover() ;

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
 
            $('#email').val(email);
            $('#name').val(name);
 
            });

   


        // Affiche dans la modal la liste des élèves du groupe sélectionné
        $('#sender_message').on('click', function (event) {
            let name = $("#name").val(); 
            let email = $("#email").val();
            let subject = $("#subject").val(); 
            let message = $("#message").val();
 
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
 
            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'name' :  name, 
                        'email' :  email,
                        'subject' :  subject,
                        'message' :  message,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "../../../ajax/sending_message_student",
                    success: function (data) {
                        console.log("teste sending");
                        alert("Vous venez d'envoyer un message à "+name+". Pour le retrouver, consulter votre boite de messages." );
                    }
                }
            )
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

                            alert("Modification enregistrée") ;

                        }
                    }
                )
            }
        });




        $('#test_students').on('click', function () {

            let students_id =  $('#students_id').val(); 

            console.log(students_id) ;

                if ( students_id != "") {  
                    alert("Vous inscrivez des élèves, chacun de vos parcours et leurs exercices leur seront affectés. Pour individualiser, il faut utiliser l'icone ad'hoc.")  ;  
                    }  
            });



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





    });
});