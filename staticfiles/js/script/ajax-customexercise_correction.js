define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-cstomexercise.js OK");

 
        // Enregistrer les commentaires
        $('.save_comment').on('click', function (event) {
            let comment = $("#comment").val();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            let student_id = $(this).attr("data-student_id");
            let customexercise_id = $(this).attr("data-customexercise_id");
            let parcours_id = $(this).attr("data-parcours_id");
            let saver = $(this).attr("data-saver");
 

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'comment': comment,
                        'student_id':student_id,
                        'exercise_id': customexercise_id,
                        'typ' : 1,
                        'parcours_id':parcours_id,
                        'saver':saver,
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
        $('#mark_evaluate').on('change', function (event) {
            let mark = $(this).val();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            let student_id = $(this).attr("data-student_id");
            let customexercise_id = $(this).attr("data-customexercise_id");
            let parcours_id = $(this).attr("data-parcours_id");

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'mark': mark,
                        'student_id':student_id,
                        'parcours_id':parcours_id,
                        'customexercise_id': customexercise_id,  
                        'custom': 1,                 
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


        // Enregistre le score de knowledge
        $('.evaluate').on('click', function (event) {
            let value = $(this).val();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            let student_id = $(this).attr("data-student_id");
            let customexercise_id = $(this).attr("data-customexercise_id");
            let parcours_id = $(this).attr("data-parcours_id");

            let knowledge_id =  $(this).attr("data-knowledge_id");
            let skill_id = $(this).attr("data-skill_id");

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'value': value,
                        'student_id':student_id,
                        'parcours_id':parcours_id,
                        'customexercise_id': customexercise_id,
                        'knowledge_id':knowledge_id,
                        'skill_id':skill_id,                        
                        'typ' : 1,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "../../../ajax_exercise_evaluate",
                    success: function (data) {
                        $('#evaluate'+student_id).html(data.eval);
                    }
                }
            )
        });


        var canvas    = document.getElementById("myCanvas");
        var ctx       = canvas.getContext('2d');
        canvas.width  = 700 ;
        canvas.height = 700;

        const value = JSON.parse(document.getElementById('this_answer').textContent); 

        console.log(value);
        
        old_Stroke = ctx.strokeStyle ; 
        ctx.lineTo(init_x,init_y);




});

});

