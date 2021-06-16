define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement ajax-ggb-score.js OK");

   $('#message_alert').css("display","none") ; 
   $('#ggb_applet_container').css("display","block") ; 
    $('#preloader').css("display","block") ; 

    $('#show_ggb').css("display","none") ; 

  $(window).on('load', function () {
    if ($('#preloader').length) {
      $('#preloader').fadeOut('slow', function () {
        $(this).remove();
      });
    }
    
  });

 
  $(window).on('load', function () {
    if ($('#preload_div').length) {
      $('#preload_div').fadeOut('slow', function () {
        $(this).remove();
        $('#show_ggb').css("display","block") ; 
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


                 if ( this_situation != numexo ) {
                        alert("Vous devez effectuer le nombre de "+situation+" situations attendues.");
                        return false;
                    }

            score = grade/(numexo-1) ;
 
            $('#numexo').val(numexo); 
            $('#score').val(score); 


        }); 





      $('#div_parcours').css("display","none") ; 


      $('#show_parcours').on('click', function (event) {

            $('#div_parcours').toggle(500) ; 


        }); 





      $('#open_draft').on('click', function (event) {

            if ($('#draft').hasClass("checkbox_no_display")) 
              { $('#draft').removeClass("checkbox_no_display") ; } 
            else 
              { $('#draft').addClass("checkbox_no_display") ; } 

        }); 



      $('#close_draft').on('click', function (event) {

            if ($('#draft').hasClass("checkbox_no_display")) 
              { $('#draft').removeClass("checkbox_no_display") ; } 
            else 
              { $('#draft').addClass("checkbox_no_display") ; } 

        }); 








    });
});