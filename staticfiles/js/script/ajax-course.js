define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-exercise_custom.js OK");



        // Affiche dans la modal le modèle pour récupérer un exercice custom
        $('.shower_course').on('click', function (event) {

            let course_id = $(this).attr("data-course_id");
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'course_id': course_id,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "parcours_shower_course",
                    success: function (data) {

                        $('#get_course_title').html(data.title);
                        $('#get_course_body').html(data.annoncement);
                    }
                }
            )
         });









        // Affiche dans la modal le modèle pour récupérer un exercice custom
        $('.getter_course').on('click', function (event) {

            let course_id = $(this).attr("data-course_id");
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'course_id': course_id,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "parcours_get_course",
                    success: function (data) {

                        $('#get_course_result').html(data.html);

                    }
                }
            )
         });






        // Affiche dans la modal le modèle pour récupérer un exercice custom
        $('#get_course_result').on('click', ".clone_to" ,  function (event) {

            let course_id = $(this).attr("data-course_id");
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            var checkbox_value = "";

                $(":checkbox").each(function () {
                    var ischecked = $(this).is(":checked");
                    if (ischecked) {
                        checkbox_value += $(this).val() + "-";
                    }
                });

                if (checkbox_value == "") { alert('Vous devez sélectionner au moins un parcours.') ;   return false ;} 

                $.ajax(
                    {
                        type: "POST",
                        dataType: "json",
                        data: {
                            'course_id': course_id,
                            csrfmiddlewaretoken: csrf_token,
                            'checkbox_value' : checkbox_value,
                        },
                        url: "parcours_clone_course",
                        success: function (data) {

                            $('#tr'+course_id).remove();

                        }
                    }
                )
         });

    });

});

