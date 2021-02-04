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




                 
 


 
    });
});