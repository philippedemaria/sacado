define(['jquery','bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-parcours.js OK");

 
 

  // Affiche dans la modal la liste des élèves du groupe sélectionné
        $('#id_level').on('change', function (event) {

            let id_level = $(this).val();
            if (id_level == " ") { alert("Sélectionner un niveau") ; return false ;}

            let id_subject = $("#id_subject").val();

            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            $("#loading").html("<i class='fa fa-spinner fa-pulse fa-fw'></i>");
            $("#loader").html("<i class='fa fa-spinner fa-pulse fa-10x fa-fw'></i>");
            $("#loading").show(); 
            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    traditional: true,
                    data: {
                        'id_level': id_level,
                        'id_subject': id_subject, 
                        'thm_id': [],                       
                        csrfmiddlewaretoken: csrf_token
                    },
                    url : "../ajax_chargethemes_quizz",
                    success: function (data) {

                        themes = data["themes"];
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


                        $('#parcours_details').html("").html(data.html);

                        $("#loading").hide(500); 
                    }
                }
            )
        });

        $('#thm_id').on('change', function (event) { 

            if (  $('select[name=level]').val() > 0 )
            {
                    let id_subject = $('#id_subject').val();
                    let id_level = $('#id_level').val();
                    if (id_level == " ") { alert("Sélectionner un niveau") ; return false ;}
                    let theme_id = $(this).val();

                    let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
                    $("#loader").html("<i class='fa fa-spinner fa-pulse fa-10x fa-fw'></i>");
                                
                    $.ajax(
                        {
                            type: "POST",
                            dataType: "json",
                            traditional: true,
                            data: {
                                'id_level': id_level,
                                'theme_id': theme_id,
                                'id_subject': id_subject,
                                csrfmiddlewaretoken: csrf_token
                            },
                            url : "../ajax_chargethemes_quizz",
                            success: function (data) {
         
                                $('#parcours_details').html("").html(data.html);
                                $("#loader").html("").hide(); 
                                
                                }
                        }
                    )
          
            }
            else 
            {   
                alert("Vous devez choisir un niveau."); return false;             
            }
        }); 

  




    });
});