define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement ajax-ggb-score.js OK");

   $('#message_alert').css("display","none") ; 
   $('#ggb_applet_container').css("display","block") ; 
    $('#preloader').css("display","block") ; 

 

  $(window).on('load', function () {
    if ($('#preloader').length) {
      $('#preloader').fadeOut('slow', function () {
        $(this).remove();
      });
    }
    
  });

 

   // Publier un cours via le menu droit
        $('#submit_button').on('click', function (event) {
          var grade = ggb_applet_container.getValue("grade");
          var numexo = ggb_applet_container.getValue("numexo");
          score = grade/(numexo-1) ;
            let start_time = $(this).attr("data-start_time");
            let exercise_id = $(this).attr("data-exercice_id"); 
 
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
 
            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'score': score,
                        'numexo': numexo-1,
                        'exercise_id':exercise_id,
                        'start_time':start_time,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "../../store_the_score_ajax/",
                    success: function () {

                        alert("Le score de cet exercice est enregistré.") ; 
                      
                        }
                }
            );
 
        }); 


 
  // Publier un cours via le menu droit
        $('#submit_button_relation').on('click', function (event) {

         console.log('#submit_button_relation on');

          var grade = ggb_applet_container.getValue("grade");
          var numexo = ggb_applet_container.getValue("numexo");
          score = grade/(numexo-1) ;

            let start_time = $(this).attr("data-start_time");
            let relation_id = $(this).attr("data-relation_id"); 
 

            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();


            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'score': score,
                        'numexo': numexo-1,
                        'relation_id':relation_id,
                        'start_time':start_time,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "../../store_the_score_relation_ajax/",
                    success: function () {
                        alert("Le score de cet exercice est enregistré.") ; 
                        }
                }
            );

        }); 


    });
});