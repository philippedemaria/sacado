define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {
 
                    console.log("=== ajax-user ===") ;

        $("#teacher_div").hide();
        $("#student_div").hide();
        $('#id_user_type').on('change', function (event) {
                if ( $('#id_user_type').val() == 2)
                    {$("#teacher_div").show(500); 
                     $("#student_div").hide(500);}
                else
                    {$("#teacher_div").hide(500); 
                     $("#student_div").show(500);}
            });


        $(".free_ins").hide();
 
        function makeItemDisappear($toggle, $item) {
                $toggle.change(function () {
                    if ($toggle.is(":checked")) {
                        $item.hide(500);
                    } else {
                        $item.show(500);
                    }
                });
            }


        makeItemDisappear($("#manual"), $(".free_ins"));
        makeItemAppear($("#id_same_section"), $("#group_choice"));
 
        function makeItemAppear($toggle, $item) {
                $toggle.change(function () {
                    if ($toggle.is(":checked")) {
                        $item.show(500);
                    } else {
                        $item.hide(500);
                    }
                });
            }


        $('#id_first_name').on('blur', function (event) {
        
                let lastname = $("#id_last_name").val();
                let firstname = $("#id_first_name").val();
                let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

                $("#id_username").val(lastname+firstname.charAt(0)) ;
                $("#id_password1").val("1234567890") ;



            $.ajax({
                url: '../ajax_usermail/',
                type :"POST",
                data: {
                    'lastname': lastname ,
                    'firstname': firstname ,
                    csrfmiddlewaretoken: csrf_token
                },
                dataType: 'json',
                success: function (data) {
                    console.log(data["html"]) ;
                    $("#id_email").val(data["html"]);
                }
            });



            });


        





    });

});