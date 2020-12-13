 
    $(document).ready(function () {
 

		 
        console.log("---- NEW test ajax-accueil.js ---") ;      


        //$('[data-toggle="popover"]').popover();
        //$(".select2").select2({width: '100%'});

        $('#teacher_form .sendit').prop('disabled', true);
        $("#teacher_form #id_username").on('blur', function () {
            let userid = $(this).val();
            console.log(userid);
            $.ajax({
                url: '/account/ajax/userinfo/',
                data: {
                    'userid': userid
                },
                dataType: 'json',
                success: function (data) {
                    $("#ajaxresultat").text(data["html"]);
                }
            });
        });


        somme = 0
        $('#teacher_form .id_first_name').on('blur', function () {

                let lastname = $("#teacher_form .id_last_name").val().toLowerCase();
                let firstname = $("#teacher_form .id_first_name").val().toLowerCase();
 
                $("#teacher_form .username").val(lastname+firstname.charAt(0)) ;
                $("#teacher_form .email").val(firstname+"."+lastname+"@") ;

                let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
                let username = lastname +  firstname  ;
    
                $.ajax({
                    url: '../account/ajax/userinfo/',
                    data: {
                        'username': username,
                        csrfmiddlewaretoken: csrf_token,                        
                    },
                    type: "POST",
                    dataType: "json",
                    success: function (data) {

                        $(".ajaxresult").html(data["html"]);
                        if (data["test"]) { $('#teacher_form .sendit').prop('disabled', false) } else { somme = somme + 1 }
                        if (somme > 1 ) { $('#teacher_form .sendit').prop('disabled', true); }  
                    }
                });
            });

 
        $('#student_form .sendit').prop('disabled', true);
        sommeS = 2
        $("#student_form #id_username").on('keyup', function () {
            let username = $(this).val();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            console.log(username);
            $.ajax({
                url: '/account/ajax/userinfo/',
                type: "POST",
                data: {
                    'username': username,
                    csrfmiddlewaretoken: csrf_token,    
                },
                dataType: 'json',
                success: function (data) {
                    $("#ajaxresultat").html(data["html"]);
                    sommeS = sommeS - 1;
                }
            });
        });

        $("#student_form #id_group").on('keyup', function () {
            let groupe_code = $(this).val();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            console.log(groupe_code);
            $.ajax({
                url: '/account/ajax/courseinfo/',
                type: "POST",
                data: {
                    'groupe_code': groupe_code,
                    csrfmiddlewaretoken: csrf_token,    
                },
                dataType: 'json',
                success: function (data) {
                    $("#student_form  .verif_course").html(data["htmlg"]);
                    sommeS = sommeS - 1;
                }
            });
        });

        $('#student_form .id_first_name').on('blur', function () {

                let lastname = $("#student_form .id_last_name").val().toLowerCase();
                let firstname = $("#student_form .id_first_name").val().toLowerCase();
 
                $("#student_form .username").val(lastname+firstname) ;

                let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
              
                let username = lastname +  firstname  ;
    
                $.ajax({
                    url: '../account/ajax/userinfo/',
                    data: {
                        'username': username,
                        csrfmiddlewaretoken: csrf_token,                        
                    },
                    type: "POST",
                    dataType: "json",
                    success: function (data) {
 
                        $(".ajaxresult").html(data["html"]);
                        if (data["test"]) {  sommeS = sommeS - 1 }  
                        if (sommeS < 1) {$('#student_form .sendit').prop('disabled', false);   } else {$('#student_form .sendit').prop('disabled', true);   }  
                    }
                });
            });


        $('.is_child_exist').prop('disabled', true);

        sommeP = 2
        $("#parent_form #id_username").on('keyup', function () {
            let username = $(this).val();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            console.log(username);
            $.ajax({
                url: '/account/ajax/userinfo/',
                type: "POST",
                data: {
                    'username': username,
                    csrfmiddlewaretoken: csrf_token,    
                },
                dataType: 'json',
                success: function (data) {
                    $("#parent_form .ajaxresultat").html(data["html"]);
                }
            });
        });


        $('#parent_form .id_first_name').on('blur', function () {

                let lastname = $("#parent_form #id_last_name").val().toLowerCase();
                let firstname = $("#parent_form #id_first_name").val().toLowerCase();
 
                $("#parent_form #id_username").val(lastname+firstname) ;
                $("#parent_form #id_email").val(firstname+"."+lastname+"@") ;


                let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
              
                let username = lastname +  firstname  ;
    
                $.ajax({
                    url: '../account/ajax/userinfo/',
                    data: {
                        'username': username,
                        csrfmiddlewaretoken: csrf_token,                        
                    },
                    type: "POST",
                    dataType: "json",
                    success: function (data) {
 
                        $("#parent_form .ajaxresult").html(data["html"]);
                        if (data["test"]) {  sommeP = sommeP - 1 }  
                        if (sommeP < 1) {$('#parent_form .is_child_exist').prop('disabled', false);   } else {$('#parent_form .is_child_exist').prop('disabled', true);   }  
                    }
                });
            });


        $('#code_student').on('keyup', function () {

                 
                let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
                let code_student =  $(this).val()  ;

                console.log(code_student) ;

                $.ajax({
                    url: '../account/ajax/control_code_student/',
                    data: {
                        'code_student': code_student,
                        csrfmiddlewaretoken: csrf_token,                        
                    },
                    type: "POST",
                    dataType: "json",
                    success: function (data) {
 
                        $("#parent_form .verif_course").html(data["html"]);
                       
                        if (data["test"]  ) {  sommeP = sommeP - 1 ; }  
                        if (sommeP < 1 ) { $('#parent_form .is_child_exist').prop('disabled', false);   }  else { $('#parent_form .is_child_exist').prop('disabled', true);   }  
                    }
                });
            });


        $("#join_alone").hide();
        $("#parcours_div").hide();
        $('#level_selected').toggle(500); 


        $("#choose_alone").click(function(){

                $('#level_choose').toggle(500);
                $('#level_selected').toggle(500); 
                $('#join_alone').toggle(500);
                $('#join_group').toggle(500); 
                $('#id_group').toggle(500); 

                if ($(this).is(":checked") && (sommeS == 1)) {    
     
                $('#send_alone').prop('disabled', false);
                } 
                else{
                $('#send_alone').prop('disabled', true);
                }
            });


        $("#send_alone").click(function(){


            level_selector = $('#level_selector').val(); 
            
            if (level_selector == "") {
                alert('Vous devez sélectionner au moins un niveau');
                return false;
            }
            });



 
        $('.family').hide() ;



        $('#one_child').click(function(){  

                $("#one_child_radio").attr("checked", "checked");
                $('#children_radio').removeAttr("checked");
                $('.child').html("").html("1 enfant"); 
                $("#one_child").addClass("btn-violet").removeClass("btn-violet_border");
                $("#children").addClass("btn-violet_border").removeClass("btn-violet");

                $('.alone').show() ;
                $('.family').hide() ;
            });


        $('#children').click(function(){

                $('#children_radio').attr("checked", "checked");
                $("#one_child_radio").removeAttr("checked");
                $('.child').html("").html("Famille");
                $("#children").addClass("btn-violet").removeClass("btn-violet_border");
                $("#one_child").addClass("btn-violet_border").removeClass("btn-violet");
                
                $('.alone').hide() ;
                $('.family').show() ;
            });


    });

 


 