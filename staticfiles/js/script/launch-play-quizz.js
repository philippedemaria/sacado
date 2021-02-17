define(['jquery',  'bootstrap', ], function ($) {
    $(document).ready(function () {
 
        console.log(" launch-play-quizz chargé "); 

        var i = 0;
        setInterval(function(){
            $("body").removeClass("bg1, bg2, bg3, bg4, bg5, bg6, bg7, bg8").addClass("bg"+(i++%8 + 1));
        }, 4000);
 

        $("#display_results").hide() ;
        // Afficher les résultats
        $(".command_results").on('click', function(){

                let all = $(this).attr("data-all");
                let question_id = $(this).attr("data-question_id");
                let random = $(this).attr("data-random");
                let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

                $.ajax(
                    {
                        type: "POST",
                        dataType: "json",
                        data: {
                            'question_id': question_id,
                            'random': random,
                            'all': all,
                            csrfmiddlewaretoken: csrf_token
                        },
                        url: "../../ajax_quizz_show_result",
                        success: function (data) {

                            $("#last_slide").hide() ;
                            $("#display_results").html(data.html) ;
                            $("#display_results").show() ;
                        }
                    }
                )
            })        





        var slideBox = $('.slider ul'),
            slideWidth = 1000 ,
            slideQuantity = $('.slider ul').children('li').length,
            currentSlide = 1 ,
            currentQuestion = 1 ;

        slideBox.css('width', slideWidth*slideQuantity);

     
        auto_play() ; 


        function timer(cible ,  duree  ){
 
                    console.log(currentSlide +" --- " + duree);

            var interval = setInterval(function() {
                duree = duree - 1000;
                document.getElementById(cible).textContent = duree/1000;

                if (( currentSlide == 2 ) && ( duree == 1000 )) {
                         
                        ajaxFn() ;
                       
                }

                // Changement de la couleur selon le temps restant
                if (duree <= 10000) { $("#"+cible).addClass("countdownOrange") ; }
                if (duree <= 5000) { $("#"+cible).removeClass("countdownOrange").addClass("countdownRed") ; }
                if (duree <= 0) { auto_play() ; clearInterval(interval); } 

            }, 1000)

            var pxValue = - (currentSlide -1) * slideWidth ; // décalage pour l'animation du slide.
            slideBox.animate({'left' : pxValue});            // Animation du slide.


            currentSlide++ ;            
        }


        function auto_play() { 
                if ( currentSlide == 1 ) 
                    {
                        duree = $("#inter_slide").val() * 1000 ;
                        timer("countdown" , duree  )
                    }
                else if ( currentSlide === 2 )   
                    {   
                        duree = $("#duration").val() * 1000 ;
                        timer("counterdown"  , duree  ) 
                    }
                else     
                    {   
                        var pxValue = - (currentSlide -1) * slideWidth ; // décalage pour l'animation du slide.
                        slideBox.animate({'left' : pxValue});            // Animation du slide. 
                        $("#counterdown").attr("id",'cdown')
                    }
 
             }


        // envoie un signal pour généré la question sur l'interface élève
        var ajaxFn = function () {

                let gquizz_id   = $("#gquizz_id").val();
                let question_id = $("#question_id").val();
                let csrf_token  = $("input[name='csrfmiddlewaretoken']").val();

 

                $.ajax({
                        type: "POST",
                        dataType: "json",
                        data:{
                                'question_id': question_id,
                                'gquizz_id'  : gquizz_id,
                                csrfmiddlewaretoken: csrf_token
                            },
                        url: "../../ajax_display_question_for_student",
                    });
            }
         
 






    });
});