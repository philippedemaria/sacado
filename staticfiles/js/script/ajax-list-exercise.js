define(['jquery',  'bootstrap' ], function ($) {
    $(document).ready(function () {
 

 	        // Affiche dans la modal le modèle pour récupérer un exercice custom
        $('.select_exercise').on('click', function (event) {

            let level_id = $(this).attr("data-level_id");
            let data_counter = $(this).attr("data-counter");
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();



            $('#'+data_counter+'a').html("<i class='fa fa-spinner fa-pulse fa-4x fa-fw'></i> <b>Chargement des exercices du niveau.</b>");



            console.log(data_counter) ; 

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

 


 
    });
});