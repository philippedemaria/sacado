define(['jquery',  'bootstrap' ], function ($) {
    $(document).ready(function () {
 
    $("#loading").hide(500); 
    console.log(" diaporama-slider chargé ");
  // Affiche dans la modal la liste des élèves du groupe sélectionné
 


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




//======================================================================================================
//====================== Vue en plein écran
//======================================================================================================
        $("#stop_quizz").hide();
        // fermer le plein écran
        $('#stop_quizz').on('click', function(){ 

            $("#navbarLeft").show(500);
            $("#stop_quizz").hide(500);
            $("#starter_quizz").show(500);
            document.fullScreenElement && null !== document.fullScreenElement || !document.mozFullScreen && !document.webkitIsFullScreen ? document.documentElement.requestFullScreen ? document.documentElement.requestFullScreen() : document.documentElement.mozRequestFullScreen ? document.documentElement.mozRequestFullScreen() : document.documentElement.webkitRequestFullScreen && document.documentElement.webkitRequestFullScreen(Element.ALLOW_KEYBOARD_INPUT) : document.cancelFullScreen ? document.cancelFullScreen() : document.mozCancelFullScreen ? document.mozCancelFullScreen() : document.webkitCancelFullScreen && document.webkitCancelFullScreen()
       
        });
        // Vue en plein écran
        $('#starter_quizz').on('click', function(){ 

            $("#navbarLeft").hide(500);
            $("#stop_quizz").show(500);
            $("#starter_quizz").hide(500);
            document.fullScreenElement && null !== document.fullScreenElement || !document.mozFullScreen && !document.webkitIsFullScreen ? document.documentElement.requestFullScreen ? document.documentElement.requestFullScreen() : document.documentElement.mozRequestFullScreen ? document.documentElement.mozRequestFullScreen() : document.documentElement.webkitRequestFullScreen && document.documentElement.webkitRequestFullScreen(Element.ALLOW_KEYBOARD_INPUT) : document.cancelFullScreen ? document.cancelFullScreen() : document.mozCancelFullScreen ? document.mozCancelFullScreen() : document.webkitCancelFullScreen && document.webkitCancelFullScreen()
       
       });
//======================================================================================================
//======================  
//======================================================================================================            
 


 
    });
});