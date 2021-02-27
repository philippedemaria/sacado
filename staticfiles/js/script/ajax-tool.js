define(['jquery',  'bootstrap'], function ($) {
    $(document).ready(function () {
 
    $("#loading").hide(500); 
    console.log(" ajax-tool chargé ");
  // Affiche dans la modal la liste des élèves du groupe sélectionné
       

 
        // Affiche dans la modal le modèle pour récupérer un exercice custom
        $('body').on('click', '.get_this_tool' , function (event) {

            let tool_id = $(this).attr("data-tool_id");
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'tool_id': tool_id,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "get_this_tool",
                    success: function (data) {

                        $('#list_of_tools').append(data.html);
                        $('#this_tool_id'+tool_id).remove();
 
                    }
                }
            )
         });

 

            var screen_size = $(window).width()  ;
 

            if($('iframe').length) { 

                width = 2.5*parseInt($('body').find("iframe").attr("width"));
                height = 2.5*parseInt($('body').find("iframe").attr("height")); 
                coeff = width/height                                    

                if (width < screen_size){
                    $('body').find("iframe").attr("width", width); 
                    $('body').find("iframe").attr("height", height);
                }
                else{
                    new_size = 0.8*screen_size ; 
                    $('body').find("iframe").attr("width", new_size ); 
                    $('body').find("iframe").attr("height", new_size / coeff );
                }
            }
       

 
     
        $('body').on('click', '.projection', function () {

            var content = $(this).html();
            var screen_size = $(window).width()  ;
 
     
                if (!$('#projection_div') ) {
                        $("body").append('<div class="projection_div"  id="projection_div" ><span class="pull-right closer_projection_div"><i class="fa fa-times fa-2x"></i></span>'+content+'</div>');                
                    }                  
         
 
                if($('#projection_div iframe').length) { 

                        width = 2.5*parseInt($('#projection_div').find("iframe").attr("width"));
                        height = 2.5*parseInt($('#projection_div').find("iframe").attr("height")); 
                        coeff = width/height ;                                    

                        if (width < screen_size){
                            $('#projection_div').find("iframe").attr("width", width); 
                            $('#projection_div').find("iframe").attr("height", height);
                        }
                        else{
                            new_size = 0.9*screen_size ; 
                            $('#projection_div').find("iframe").attr("width", new_size ); 
                            $('#projection_div').find("iframe").attr("height", new_size / coeff );
                        }
                    }
 

        });


        $("#stop_quizz").hide();
        // fermer le plein écran
        $('#stop_quizz').on('click', function(){ 

            $("#content_title_page").show(500);
            $("#navbarLeft").show(500);
            $("#stop_quizz").hide(500);
            $("#starter_quizz").show(500);
            document.fullScreenElement && null !== document.fullScreenElement || !document.mozFullScreen && !document.webkitIsFullScreen ? document.documentElement.requestFullScreen ? document.documentElement.requestFullScreen() : document.documentElement.mozRequestFullScreen ? document.documentElement.mozRequestFullScreen() : document.documentElement.webkitRequestFullScreen && document.documentElement.webkitRequestFullScreen(Element.ALLOW_KEYBOARD_INPUT) : document.cancelFullScreen ? document.cancelFullScreen() : document.mozCancelFullScreen ? document.mozCancelFullScreen() : document.webkitCancelFullScreen && document.webkitCancelFullScreen()
       
        });
        // Vue en plein écran
        $('#starter_quizz').on('click', function(){ 

            $("#content_title_page").hide(500);
            $("#navbarLeft").hide(500);
            $("#stop_quizz").show(500);
            $("#starter_quizz").hide(500);
            document.fullScreenElement && null !== document.fullScreenElement || !document.mozFullScreen && !document.webkitIsFullScreen ? document.documentElement.requestFullScreen ? document.documentElement.requestFullScreen() : document.documentElement.mozRequestFullScreen ? document.documentElement.mozRequestFullScreen() : document.documentElement.webkitRequestFullScreen && document.documentElement.webkitRequestFullScreen(Element.ALLOW_KEYBOARD_INPUT) : document.cancelFullScreen ? document.cancelFullScreen() : document.mozCancelFullScreen ? document.mozCancelFullScreen() : document.webkitCancelFullScreen && document.webkitCancelFullScreen()
       
       });










 
    });
});