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

 
 


        $('#submit_button_relation').on('click', function (event) {

          var grade = ggb_applet_container.getValue("grade");
          var numexo = ggb_applet_container.getValue("numexo");
           let situation = $("#situation").val() ;


           numexo = parseInt(numexo)  ;
           this_situation = parseInt(situation) ;

                if ( situation  > numexo ) {
                        alert("Vous devez atteindre "+situation+" situations pour enregistrer le résultat.");
                        return false;
                    }

            score = grade/(numexo-1) ;
 
            $('#numexo').val(numexo); 
            $('#score').val(score); 


        }); 




        $('#submit_button_evaluation').on('click', function (event) {

          var grade = ggb_applet_container.getValue("grade");
          var numexo = ggb_applet_container.getValue("numexo");
           let situation = $("#situation").val() ;

           grade = parseInt(grade) ;
           numexo = parseInt(numexo)  ;

           var this_situation = parseInt(situation)  + 1 ;

           console.log(situation  , numexo , this_situation ) ; 

                 if ( this_situation != numexo ) {
                        alert("Vous devez effectuer le nombre de "+situation+" situations attendues.");
                        return false;
                    }



            score = grade/(numexo-1) ;
 
            $('#numexo').val(numexo); 
            $('#score').val(score); 


        }); 






















    });
});