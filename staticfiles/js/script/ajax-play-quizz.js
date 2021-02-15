define(['jquery',  'bootstrap', ], function ($) {
    $(document).ready(function () {
 
        console.log(" ajax-play-quizz chargé ");

 
        var i = 0;
        setInterval(function(){
            $("body").removeClass("bg1, bg2, bg3, bg4, bg5, bg6, bg7, bg8").addClass("bg"+(i++%8 + 1));
        }, 4000);
 

        // Affiche dans la modal le modèle pour récupérer un exercice custom
        $('body').on('click', '.selector_slide' , function (event) {


            let diaporama_id = $("#diaporama_id").val();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();  console.log(diaporama_id) ; 

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'diaporama_id': diaporama_id,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "../get_question_type",
                    success: function (data) {

                        $('#body_question').html(data.html);
                        $('#type_of_question_in_title').html(data.title);
 
                    }
                }
            )
         });




    });
});