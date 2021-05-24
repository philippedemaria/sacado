define(['jquery',  'bootstrap' ], function ($) {
    $(document).ready(function () {
 

 	        // Affiche dans la modal le modèle pour récupérer un exercice custom
        $('.select_exercise').on('click', function (event) {

            let level_id = $(this).attr("data-level_id");

            if (level_id == " ") { alert("Sélectionner un niveau") ; return false ;}

            let data_counter = $(this).attr("data-counter");
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            $('#'+data_counter+'a').html("<i class='fa fa-spinner fa-pulse fa-4x fa-fw'></i> <b>Chargement des exercices du niveau.</b>");

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'level_id': level_id,
                        'data_counter': data_counter,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "ajax_list_exercises_by_level",
                    success: function (data) {

                        $('#'+data_counter+'a').html("").html(data.html);
 
                    }
                }
            )
         });

       
  // Affiche dans la modal la liste des élèves du groupe sélectionné
        $('#id_level').on('change', function (event) {
            let id_level = $(this).val();
            if (id_level == " ") { alert("Sélectionner un niveau") ; return false ;}
            let id_subject = $("#id_subject").val();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            $("#loader").html("<i class='fa fa-spinner fa-10x fa-pulse fa-fw'></i><br/>Chargement...");
            $("#loader").show(); 

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
                    url : "ajax/chargethemes_exercise",
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

                        $('#content_exercises').html("").html(data.html);
                        $("#loader").hide(500); 


                   }
                }
            )
        });




        $('#id_theme').on('change', function (event) {

            if (  $('select[name=level]').val() > 0 )
            {
                ajax_choice($('select[name=level]'),$('select[name=theme]')) ;            
            }
            else 
            {   
                alert("Vous devez choisir un niveau."); return false;             
            }
        }); 



        function ajax_choice(param0, param1){

            let is_parcours = $("#is_parcours").val();
            let level_id = param0.val();
            let theme_id = param1.val();
            let subject_id = $("#id_subject").val(); 

            $("#loading").html("<i class='fa fa-spinner  fa-pulse fa-fw'></i>");
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            var parcours_id = $("#id_parcours").val();

            if($("#loader")) {$("#loader").html("<i class='fa fa-spinner fa-pulse fa-10x fa-fw'></i>");      }

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    traditional: true,
                    data: {
                        'parcours_id': parcours_id ,
                        'level_id': level_id,
                        'theme_id': theme_id,
                        'subject_id': subject_id,

                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "ajax_list_exercises_by_level_and_theme",
                    success: function (data) {
 
                        $('#content_exercises').html("").html(data.html);
                        $("#loader").html(""); 
                        $("#loading").hide(500); 
                        }
                }
            )

        }

      


 
    });
});