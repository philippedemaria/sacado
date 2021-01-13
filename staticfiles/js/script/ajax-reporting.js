define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-course.js OK");



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
                        $('#get_course_body').html(data.html);
                        $('#document_id').val(course_id);

                    }
                }
            )
         });














    });

});

