 $(document).ready(function()
	{


		console.log("---- NEW test ajax-accueil.js ---") ;		

 
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
                    $("#student_form .ajaxresult").html(data["html"]);
                    sommeS = sommeS - 1;
                }
            });
        });

        $("#student_form #id_group").on('keyup', function () {
            let groupe_code = $(this).val();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
 
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



        $('#student_form .id_last_name').on('blur', function () {

                let lastname = $("#student_form .id_last_name").val().replace(" ","").toLowerCase();
                let firstname = $("#student_form .id_first_name").val().replace(" ","").toLowerCase();
 
                $("#student_form .username").val(firstname+"."+lastname) ;

                let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
              
                let username = firstname +"."+  lastname  ;
    
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




        $("#already").hide();
        $("#new_inscription").hide();

 
        $('#show_already').on('click', function (event) { 
            $("#new_inscription").hide();
            $('#already').show(); 
            $('#already').removeClass("no_display"); 
            $('.remove_after').remove();
            $('.init_box').removeClass("init_box"); 
            $('#show_already').addClass("btn btn-default"); 
            $('#show_new_inscription').addClass("btn btn-default"); 
        });

 
        $('#show_new_inscription').on('click', function (event) { 
            $("#new_inscription").show();
            $('#already').hide(); 
            $('#new_inscription').removeClass("no_display"); 
            $('.remove_after').remove(); 
            $('.init_box').removeClass("init_box");
            $('#show_new_inscription').addClass("btn btn-default"); 
            $('#show_already').addClass("btn btn-default"); 
        });



});

 