define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {

        console.log("chargement JS get-school.js OK");
 
        setTimeout(function(){ 
           $("#container_messages").css('display', "none"); 
        }, 3000);

        $("#show_form_teacher").hide() ;
        $("#select_rne").hide();

        $('#show_from_here').on('click', function (event) {
            $("#show_here").toggle(300) ;
        });
  


 
        $("#show_get_school_div").hide();

        $('#get_school_div').on('click', function (event) {
            $("#show_get_school_div").toggle(300) ;
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
                    url : "../account/ajax_charge_town/",
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

                            { 

                               let option_null = $("<option>", {  'value': "", 'html': "--------Choisir----------" });
                                    $('select[name=town_school]').append(option_null);
                             
                             


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
                    url : "../account/ajax_charge_school/",
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
                    url : "../account/ajax_charge_school_by_rne/",
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
});

 
