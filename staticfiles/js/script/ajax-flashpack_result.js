define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-customexercise.js OK");

 
        // Enregistrer les commentaires
        $('.select_student').on('click', function (event) {

            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            let student_id = $(this).data("student_id");
            let flashpack_id = $(this).data("flashpack_id");
 
 

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'flashpack_id': flashpack_id,
                        'student_id':student_id,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "../../ajax_results_flashpack",
                    success: function (data) {
                        $('#result_div').html("").html(data.html);
                    } 
                }
            )
        });





});

});

