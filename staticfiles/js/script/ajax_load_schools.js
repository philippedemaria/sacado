define(['jquery', 'bootstrap' ], function ($) {
    $(document).ready(function () {
 
 
        console.log("---- NEW test ajax-load_school.js ---") ;  






        $('#show_from_here').on('click', function (event) {
            $("#show_here").toggle(300) ;
        });
        $("#select_rne").hide();

        $("#show_form_teacher").hide();


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
                    url : "ajax_charge_town",
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
                    url : "ajax_charge_school",
                    success: function (data) {



                        $("#id_school").html(data["html"]);
                        
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
                    url : "ajax_charge_school_by_rne",
                    success: function (data) {


                        $("#id_school").html(data["html"]);


                        
                    }
                }
            )
        });

});
});

 
