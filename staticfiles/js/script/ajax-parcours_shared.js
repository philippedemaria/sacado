define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-parcours_shared.js OK");
 





        // Affiche dans la modal la liste des élèves du groupe sélectionné
        $('#id_level').on('change', function (event) {



            let id_level = $(this).val();
            let id_subject = $("#id_subject").val();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            $("#loading").html("<i class='fa fa-spinner fa-pulse fa-fw'></i>");
            $("#loading").show(); 


            if (id_level > 0)
            {
                $.ajax(
                    {
                        type: "POST",
                        dataType: "json",
                        traditional: true,
                        data: {
                            'id_level': id_level,
                            'id_subject': id_subject,                        
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

                            $("#loading").html("").hide(500); 
                        }
                    }
                )                
            }

        });
 



 
        $('select[name=theme]').on('change', function (event) {

            if (  $('select[name=level]').val() > 0 )
            {
                ajax_choice($('select[name=level]'),$('select[name=theme]')) ;            
            }
            else 
            {   
                alert("Vous devez choisir un niveau."); return false;             
            }

        }); 


        $('select[name=level]').on('change', function (event) {

                ajax_choice($('select[name=level]'),$('select[name=theme]')) ;            
        });






        function ajax_choice(param0, param1){

 

            if ( param0.val() > 0 ) {var level_id = param0.val() ; console.log(level_id) ;  } else {var level_id = 0 ; console.log(level_id) ; }  
            if ( param1.val() > 0  ) {var theme_id = param1.val() ; console.log(theme_id) ; } else {var theme_id = [] ; console.log(theme_id) ; }  
 
            let is_eval = $("#is_eval").val();
            let subject_id = $("#id_subject").val();
            let keywords = $("#keywords").val();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
 
            $("#loader").html("<i class='fa fa-spinner fa-pulse fa-3x fa-fw'></i>");
            
 

            $.ajax(
                    {
                    type: "POST",
                    dataType: "json",
                    traditional: true,
                    data: {
                        'is_eval'      : is_eval,
                        'subject_id'   : subject_id,
                        'level_id'     : level_id,
                        'theme_id'     : theme_id,
                        'keywords'     : keywords,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url:"../../ajax_all_parcourses",
                    success: function (data) {
 
                        $('#courses_details').html("").html(data.html);
                        $("#loader").html("").hide(); 
                        
                        }
                    }
                )

            }



 
        $('#keywords').on('keyup', function (event) {

            ajax_choice($('select[name=level]'),$('select[name=theme]')) ;

        }); 







    });

});

