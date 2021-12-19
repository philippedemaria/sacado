define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-customexercise.js OK");

 
 

        var show_toggle = 0;

        $("#show_result_criterions").on('click', function (event) {

            $("#div_result_criterions").toggle();
            if (show_toggle%2==1){ $("#label_result_criterions").html("Cacher les critères") } else { $("#label_result_criterions").html("Afficher les critères") }

            show_toggle++ ;
        })


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
        canvas.width  = "100%" ;
        canvas.height = 800;
        new_color = "#000000" ;


        if (document.getElementById('this_answer') !== null )
            { const value = JSON.parse(document.getElementById('this_answer').textContent); }
        else { const value = "" ;}


        function draw_line(value) {

            if (value !="") {


                segments = value.split("=");
                segments.forEach( position );


                function position(item) {


                    positions = item.split("!") ;
                    ctx.strokeStyle = "#000000" ;
            
                    ctx.beginPath();
                    positions.forEach(create_draw);
                    ctx.stroke();
                    ctx.closePath(); 


                        function create_draw(itemize,index) {
                
                                if (index > 0) // empeche la récupération de la balise d'entrée
                
                                 { 
                                    coords = itemize.split(",");
                
                                    if (coords[0] != "") 
                                        { new_color = coords[0]; }
                
                                    ctx.strokeStyle = new_color ;
          
                                     ctx.lineTo(coords[1],coords[2]);
     
                                }
                            
                            }
            
                    }



                }


                // var socket = new WebSocket('ws://' + window.location.host + '/ws/qcm/')

                // socket.onmessage = function(event){
                //     var data = JSON.parse(event.data);

                //     console.log(data);

                //     document.querySelector('#app').innerText = data.listing ;

                // }
 

        }

         setInterval(get_value, 4000)


 
         function get_value() {
 
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            let student_id = $("#student_id").val();
            let customexercise_id = $("#customexercise_id").val();
            let parcours_id = $("#parcours_id").val();
 

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
 
                        'student_id':student_id,
                        'parcours_id':parcours_id,
                        'customexercise_id': customexercise_id,
 
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "../../../get_values_canvas",
                    success: function (data) {

                        draw_line(data.values);
                        
                    }
                }
            )
        } 










});

});

