define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-exercise.js OK");

 

        // Enregistrer les commentaires
        $('.save_comment').on('click', function (event) {
            let comment = $("#comment").val();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            let student_id = $(this).attr("data-student_id");
            let relationship_id = $(this).attr("data-relationship_id");
            let saver = $(this).attr("data-saver");
 
            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'comment': comment,
                        'student_id':student_id,
                        'exercise_id': relationship_id, 
                        'saver': saver,                     
                        'typ' : 0,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "../../../ajax_comment_all_exercise",
                    success: function (data) {
                        $('#comment_result').html(" enregistré");
                    } 
                }
            )
        });




        // Enregistre le score de knowledge
        $('input[name=knowledge]').on('click', function (event) {
            let value = $(this).val();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            let student_id = $(this).attr("data-student_id");
            let relationship_id = $(this).attr("data-relationship_id");

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'value': value,
                        'student_id':student_id,
                        'relationship_id': relationship_id,
                        'typ' : 0,
                        'knowledge_id': 1,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "../../../ajax_exercise_evaluate",
                    success: function (data) {
                        $('#evaluate'+student_id).html(data.eval);
                    }
                }
            )
        });




        // Enregistre le score de knowledge
        $('.evaluate').on('click', function (event) {
            let value = $(this).val();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            let student_id = $(this).attr("data-student_id");
            let relationship_id = $(this).attr("data-relationship_id");
            let skill_id = $(this).attr("data-skill_id");

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'value': value,
                        'student_id':student_id,
                        'skill_id':skill_id,
                        'relationship_id': relationship_id,
                        'typ' : 0,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "../../../ajax_exercise_evaluate",
                    success: function (data) {
                        $('#evaluate'+student_id).html(data.eval);
                    }
                }
            )
        });


        // Enregistre le score de knowledge
        $('#mark_evaluate').on('change', function (event) {
            let mark = $(this).val();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            let student_id = $(this).attr("data-student_id");
            let relationship_id = $(this).attr("data-relationship_id");

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'mark': mark,
                        'student_id':student_id,
                        'custom': 0,
                        'relationship_id': relationship_id,                        
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "../../../ajax_mark_evaluate",
                    success: function (data) {
                        $('#evaluate'+student_id).html(data.eval);
                        $('#mark_sign').html(data.eval);

                    }
                }
            )
        });




});

});

