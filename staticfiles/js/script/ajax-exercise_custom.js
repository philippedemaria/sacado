define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-exercise_custom.js OK");


        // Affiche dans la modal le modèle pour récupérer un exercice custom
        $('.getter_exercice_custom').on('click', function (event) {

            let exercise_id = $(this).attr("data-exercise_id");
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'exercise_id': exercise_id,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "parcours_get_exercise_custom",
                    success: function (data) {

                        $('#get_exercice_result').html(data.html);

                    }
                }
            )
         });


        // Affiche dans la modal le modèle pour récupérer un exercice custom
        $('#get_exercice_result').on('click', ".clone_to" ,  function (event) {

            let exercise_id = $(this).attr("data-exercise_id");
            let cloner = $(this).attr("data-cloner");
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            var checkbox_value = "";

                $(":checkbox").each(function () {
                    var ischecked = $(this).is(":checked");
                    if (ischecked) {
                        checkbox_value += $(this).val() + "-";
                    }
                });

                if ( cloner == 1 ) { if (checkbox_value == "") { alert('Vous devez sélectionner au moins un parcours.') ;   return false ;} }

                $.ajax(
                    {
                        type: "POST",
                        dataType: "json",
                        data: {
                            'exercise_id': exercise_id,
                            csrfmiddlewaretoken: csrf_token,
                            'checkbox_value' : checkbox_value,
                        },
                        url: "parcours_clone_exercise_custom",
                        success: function (data) {

                            $('#tr_custom'+exercise_id).remove();

                        }
                    }
                )
         });

    });

});

