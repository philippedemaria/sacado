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
 

            if($('#projection_div iframe').length) { 

                width = 2*parseInt($('#projection_div').find("iframe").attr("width"));
                height = 2*parseInt($('#projection_div').find("iframe").attr("height")); 
                coeff = width/height                                    

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
});