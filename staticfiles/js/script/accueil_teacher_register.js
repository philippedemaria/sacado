 
    $(document).ready(function () {
 

  
 
        console.log("---- NEW test accueil_teacher_register.js ---") ;  




        setTimeout(function(){ 
           $("#container_messages").css('display', "none"); 
        }, 3000);

        //$('[data-toggle="popover"]').popover();
        //$(".select2").select2({width: '100%'});

        $('.sendit').prop('disabled', true);
 
        $("#id_username").on('blur', function () {
            let username = $(this).val();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            console.log(username);
            $.ajax({
                url: '/account/ajax/userinfo/',
                data: {
                    'username': username,
                    'csrf_token' : csrf_token ,
                },
                type: "POST",
                dataType: "json",
                success: function (data) {
                    $(".ajaxresult").html(data["html"]);

                    if(data["test"]) { $(".sendit").prop("disabled", false ) ;} else { $(".sendit").prop("disabled", true ) ;}
                }
            });
        });

        $("#id_email").on('blur', function () {

            let email = $(this).val();
            filtre_mail_academique = /^[a-z0-9_\.\-]+@ac-[a-z]*\.fr$/i ; 
            filtre_mail_aefe = /^[a-z0-9_\.\-]+@aefe.fr$/i ; 
            filtre_mail_education = /^[a-z0-9_\.\-]+@education.lu$/i ; 
            filtre_mail_mlf = /^[a-z0-9_\.\-]+@mlfmonde.org$/i ;

            if ( (filtre_mail_education.test( email )) || (filtre_mail_aefe.test( email )) || (filtre_mail_academique.test( email ))  || (filtre_mail_mlf.test( email )) )  { 


                let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
     
                $.ajax({
                    url: '/account/ajax/userinfomail/',
                    data: {
                        'email': email,
                        'csrf_token' : csrf_token ,
                    },
                    type: "POST",
                    dataType: "json",
                    success: function (data) {
                        $(".ajaxresultmail").html(data["html"]);

                        if(data["test"]) { $(".sendit").prop("disabled", false ) ;} else { $(".sendit").prop("disabled", true ) ;}
                    }
                });
               
            }
            else
            {
                alert(" Vous devez utiliser une adresse académique @ac-****.fr ou @aefe.fr  ou nous contacter.") ; $(".sendit").prop("disabled", true ) ; 
            }

        });



        somme = 0
        $('.id_first_name').on('blur', function () {

                let lastname = $(".id_last_name").val().toLowerCase();
                let firstname = $(".id_first_name").val().toLowerCase();
 
                $(".username").val(lastname+firstname.charAt(0)) ;
                $(".email").val(firstname+"."+lastname+"@") ;

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
                        if (data["test"]) { $('.sendit').prop('disabled', false) } else { somme = somme + 1 }
                        if (somme > 1 ) { $('.sendit').prop('disabled', true); }  
                    }
                });
            });

 

        $("#show_form_teacher").hide() ;
        $("#select_rne").hide();

        $('#show_from_here').on('click', function (event) {
            $("#show_here").toggle(300) ;
        });
  

        $('#id_country_school').on('change',  function (event) {    

            let id_country_school = $(this).val(); 
 
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    traditional: true,
                    data: {
                        'id_country': id_country_school,                      
                        csrfmiddlewaretoken: csrf_token
                    },
                    url : "ajax_charge_town/",
                    success: function (data) {

                        towns = data["towns"] ;
                        id_country = data["id_country"];

                        if ( id_country == '5')
                        { 
                            $("#select_rne").show();        
                            $("#select_town").hide();       
                        }
                        else
                        {   
                            $("#select_rne").hide();
                            $('select[name=town_school]').empty("");
                            $("#select_town").show();

                            if (towns.length >0)

                            { if (towns.length == 1 )
                                {   let option_null = $("<option>", {  'value': "", 'html': "--------Choisir----------" });
                                    $('select[name=town_school]').append(option_null);
                                }


                                for (let i = 0; i < towns.length ; i++) {            
                                    let town       = towns[i][0];  
                                    let towns_name = towns[i][1];   
                                    let option = $( "<option>"  ,  { 'value':  town , 'html': towns_name }    );
                                    $('select[name=town_school]').append(option);
                                }
                            }
                            else
                            {
                                let option = $("<option>", {
                                    'value': "",
                                    'html': "Aucun contenu disponible"
                                });
                                $('select[name=town_school]').append(option);
                            }
                        }
 
        


                        
                    }
                }
            )
        });





        $('#id_town_school').on('change', function (event) {

            let id_country = $("#id_country_school").val();
            let id_town = $(this).val();
            if (id_town == " ") { alert("Sélectionner une ville") ; return false ;}
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    traditional: true,
                    data: {
                        'id_town'   : id_town,  
                        'id_country': id_country,                      
                        csrfmiddlewaretoken: csrf_token
                    },
                    url : "ajax_charge_school/",
                    success: function (data) {

                        $('select[name=school]').empty("");                        
                        schools = data["schools"] ;
                        if (schools.length >0)

                        { for (let i = 0; i < schools.length; i++) {
                                    
                                let school_id   = schools[i][0];
                                let school_name = schools[i][1]  ;
                                let option = $("<option>", {  'value': Number(school_id), 'html': school_name });
                                $('select[name=school]').append(option);
                            }
                        }
                        else
                        {
                            let option = $("<option>", {  'value': "", 'html': "Aucun contenu disponible" });
                            $('select[name=school]').append(option);  
                        }


                        $("#show_form_teacher").show();
                        
                    }
                }
            )
        });





        $('#id_rne').on('change', function (event) {

            let id_rne = $(this).val();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    traditional: true,
                    data: {
                        'id_rne'   : id_rne,                      
                        csrfmiddlewaretoken: csrf_token
                    },
                    url : "ajax_charge_school_by_rne/",
                    success: function (data) {

                        $('select[name=school]').empty("");                        
                        schools = data["schools"] ;
                        if (schools.length >0)

                        { for (let i = 0; i < schools.length; i++) {
                                    
                                let school_id   = schools[i][0];
                                let school_name = schools[i][1]  ;
                                let option = $("<option>", {  'value': Number(school_id), 'html': school_name });
                                $('select[name=school]').append(option);
                            }
                        }
                        else
                        {
                            let option = $("<option>", {  'value': "", 'html': "Aucun contenu disponible" });
                            $('select[name=school]').append(option);  
                        }


                        $("#show_form_teacher").show();
                        
                    }
                }
            )
        });



});

 
