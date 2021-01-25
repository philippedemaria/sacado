define(['jquery',  'bootstrap' ], function ($) {
    $(document).ready(function () {
 
 
        console.log(" ajax-slider chargé ");




        var slideBox = $('.slider ul'),
            slideWidth = 800 ,
            slideQuantity = $('.slider ul').children('li').length,
            currentSlide = 1 ,
            currentQuestion = 1 ;

        slideBox.css('width', slideWidth*slideQuantity);

     
        function transition(currentSlideInput, slideWidthInput){

            var pxValue = -(currentSlideInput -1) * slideWidthInput ; 
            slideBox.animate({
                'left' : pxValue
            })
        }



       $('.nav button').on('click', function(){ 

               var whichButton = $(this).data('nav'); 
               console.log(whichButton);

                   if (whichButton === 'next') {

                        if (currentSlide === slideQuantity)
                            { 
                                currentSlide = 1 ; 
                            }
                        else 
                            { 
                                currentSlide++ ; 
                            }
                        transition(currentSlide, slideWidth )  ;


                   } else if (whichButton === 'prev') {

                        if (currentSlide === 1)
                            { 
                                currentSlide = slideQuantity ; 
                            }
                        else 
                            { 
                                currentSlide-- ; 
                            }
                        transition(currentSlide, slideWidth ) ;
                   }

            });


                var starter_play = 0;
                $('#start_quizz').on('click', function(){
 

                        if (starter_play%2 ===0) {

                            $("#start_quizz").html("").html("<button  class='btn btn-danger'><i class='fa fa-stop'></i> Arrêter</button>") ;
                            auto_play() ;

                        }
                        else
                        {  

                            $("#start_quizz").html("").html("<button  class='btn btn-default'><i class='fa fa-play'></i> Démarrer</button>") ;
                             clearInterval(interval);
                        }
                            starter_play++ ;

                       })  
 



                    step  = 0 ;
                    function auto_play(){

                            if (currentSlide === slideQuantity) // Si on arrive au bout du nombre de slides, le quizz s'arrete.
                                { 
                                    $("#start_quizz").html("").html("<button  class='btn btn-default'><i class='fa fa-play'></i> Démarrer</button>") ;
                                    clearInterval(interval);
                                }
                            else  // Si on avance d'une slide à chaque fois.
                                { 
                                    currentSlide++ ;
                                }

                            var pxValue = - (currentSlide -1) * slideWidth ; // décalage pour l'animation du slide.
                            slideBox.animate({'left' : pxValue});            // Animation du slide.

                            $(".btn").removeClass("btn-primary").addClass("btn-default")  ;   // Couleurs des boutons

                            if ( step === 0 )  // Introduction du quizz
                            {
                                this_slide =  0 ; 
                                duree = $("#introduction").val() * 1000 ; // Durée de l'introduction
                                $("#question1").addClass("btn-primary").removeClass("btn-default")  ;    // Couleurs des boutons
                            }
                            else  // Lecture des diapo des questions
                            {
                                this_slide = parseInt( (currentSlide-1)/2) ; // Sélection du temps entre les dipa ou de la diapo
                                if ( step%2 === 0 ) 
                                    {
                                        duree = $("#inter_slide"+this_slide).val() * 1000 ;                            
                                    }
                                    else   
                                    {
                                        duree = $("#duration"+this_slide).val() * 1000 ;                        
                                    }


                                 // Couleurs des boutons déjà des questions déjà travaillées
                                currentQuestion++ ; 
                                this_question = parseInt( (currentQuestion+1)/2) ;
                                for (col=1;col<this_question;col++){ $("#question"+col).addClass("btn-success").removeClass("btn-default")  ;  }
                                 // Seule la question en cours en bleu
                                $("#question"+this_question).addClass("btn-primary").removeClass("btn-default")  ;  

                                }
 

                            interval = setTimeout(auto_play, parseInt(duree) ); // la fonction auto_play se relance avec un temps différent
                            step ++ ;

                        }

 

                    



    });
});