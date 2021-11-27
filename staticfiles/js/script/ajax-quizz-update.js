define(['jquery',  'bootstrap' ], function ($) {
    $(document).ready(function () {
 
 
    console.log(" ajax-quizz-update chargé ");
 
    qtype = $("#qtype").val() ;
 
 

function is_cheched_update(nb){
               if ($("#id_choices-"+nb+"-is_correct").is(":checked"))
                {
                    $("#noCheck"+nb).hide() ;
                    $("#check"+nb).show() ;
                }
            else
                {
                    $("#noCheck"+nb).show() ;
                    $("#check"+nb).hide() ;
                } 
}



 
  if (qtype == 0)
    {
            is_cheched_update(0);
            is_cheched_update(1);
    }
    else if (qtype > 2)
    {
           
        is_cheched_update(0);
        is_cheched_update(1);
        is_cheched_update(2);
        is_cheched_update(3);

        $("#answer0_div").addClass("bgcolorRed");
        $("#answer1_div").addClass("bgcolorBlue");
        $("#answer2_div").addClass("bgcolorOrange");
        $("#answer3_div").addClass("bgcolorGreen");
 
    }



    });
});