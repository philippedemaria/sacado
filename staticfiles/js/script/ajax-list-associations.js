define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {
 
 console.log("ajax-associations chargé") ;

        // Affiche dans la modal la liste des élèves du groupe sélectionné
        $('.create_association').on('click', function (event) {

            let exercise_id = $(this).attr("data-exercise_id");
            let code = $("#create_code"+exercise_id).val();
            let action = $(this).attr("data-action");
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            console.log(exercise_id+"----"+action+"----"+code);

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'code': code,
                        'exercise_id': exercise_id,
                        'action': action,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "../ajax_update_association",
                    success: function (data) {

                        $("#row"+exercise_id).append(data.html) ;
                        $("#error_str"+exercise_id).html("").append(data.error) ;
                       
                    }
                }
            )
        });




        // Affiche dans la modal la liste des élèves du groupe sélectionné
        $('.update_association').on('click', function (event) {

            let exercise_id = $(this).attr("data-exercise_id");
            let action = $(this).attr("data-action");
            let code = $("#update_code"+exercise_id).val();
                if (code == "") { alert("Vous devez renseigner le code d'un support."); return false; }                
                if (!confirm("Vous souhaitez modifier l'association avec ce support "+code+" ?")) return false; 
           

            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            console.log(exercise_id+"----"+action+"----"+code);

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'code': code,
                        'exercise_id': exercise_id,
                        'action': action,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "../ajax_update_association",
                    success: function (data) {

                        $("#association"+exercise_id).html("").append(data.html) ;
                        $("#error_str"+exercise_id).html("").append(data.error) ;

                    }
                }
            )
        });








        // Affiche dans la modal la liste des élèves du groupe sélectionné
        $('.delete_association').on('click', function (event) {

            let exercise_id = $(this).attr("data-exercise_id");
            let action = $(this).attr("data-action");
            if (!confirm("Vous souhaitez supprimer l'association avec ce support ?")) return false;  
     

            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            console.log(exercise_id+"----"+action);

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'exercise_id': exercise_id,
                        'action': action,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "../ajax_update_association",
                    success: function (data) {

                        $("#new_exercice"+exercise_id).remove() ;
                    }
                }
            )
        });










 
    });
});