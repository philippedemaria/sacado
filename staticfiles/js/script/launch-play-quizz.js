define(['jquery',  'bootstrap', ], function ($) {
    $(document).ready(function () {
 
        console.log(" ajax-quizz-teacher chargé "); 

        var i = 0;
        setInterval(function(){
            $("body").removeClass("bg1, bg2, bg3, bg4, bg5, bg6, bg7, bg8").addClass("bg"+(i++%8 + 1));
        }, 4000);
 


        var slideBox = $('.slider ul'),
            slideWidth = 1000 ,
            slideQuantity = $('.slider ul').children('li').length,
            currentSlide = 1 ,
            currentQuestion = 1 ;

        slideBox.css('width', slideWidth*slideQuantity);

     
        function transition(currentSlideInput, slideWidthInput){

            var pxValue = -(currentSlideInput -1) * slideWidthInput ; 
            slideBox.animate({
                'left' : pxValue
            })
            this_question = parseInt( (currentSlideInput+1)/2)-1 ;

            $(".this_question").addClass("btn-default").removeClass("btn-primary") ;
            $("#question"+this_question).removeClass("btn-default").addClass("btn-primary") ;
        }



       $('.nav button').on('click', function(){ 

        $(".instruction").hide();

               var whichButton = $(this).data('nav'); 

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


                var starter_play = 0 ,
                    step         = 0 ,
                    now          = 0 ,
                    step_count   = 0;

                $('#start_quizz').on('click', function(){

                            $(".instruction").show();
 

                        if ( starter_play%2 === 0 ) {

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

                            $(".thisquestion").removeClass("btn-primary").addClass("btn-default")  ;   // Couleurs des boutons

                            if ( step === 0 )  // Introduction du quizz
                            {
                                this_slide =  0 ; 
                                duree = $("#introduction").val() * 1000 ; // Durée de l'introduction
                                $("#question1").addClass("btn-primary").removeClass("btn-default")  ;    // Couleurs des boutons
                                step ++ ;
                                interval = setTimeout(auto_play, parseInt(duree) ); // la fonction auto_play se relance avec un temps différent
                            }
                            else  // Lecture des diapo des questions
                            {
                                this_slide = parseInt( (currentSlide-1)/2) ; // Sélection du temps entre les dipa ou de la diapo
                                if ( step%2 === 0 ) 
                                    {
                                        duree = $("#inter_slide"+this_slide).val() * 1000 ;
                                        step ++ ;
                                        interval = setTimeout(auto_play, parseInt(duree) ); // la fonction auto_play se relance avec un temps différent             
                                    }
                                    else   
                                    {   
                                        duree = $("#duration"+this_slide).val() * 1000 ;

                                        var interval = setInterval(function() {
                                            duree = duree - 1000;
                                            document.getElementById("countdown"+this_slide).textContent = duree/1000;

                                            // Changement de la couleur selon le temps restant
                                            if (duree <= 10000) { $("#countdown"+this_slide).addClass("countdownOrange") ; }
                                            if (duree <= 5000) { $("#countdown"+this_slide).removeClass("countdownOrange").addClass("countdownRed") ; }
                                            if (duree <= 0) { auto_play() ; clearInterval(interval); }

                                        }, 1000);


                                    }


                                 // Couleurs des boutons déjà des questions déjà travaillées
                                currentQuestion++ ; 
                                this_question = parseInt( (currentQuestion+1)/2) ;
                                for (col=1;col<this_question;col++){ $("#question"+col).addClass("btn-success").removeClass("btn-default")  ;  }
                                 // Seule la question en cours en bleu
                                $("#question"+this_question).addClass("btn-primary").removeClass("btn-default")  ;  

                            }

                            
                        }
 




    });
});