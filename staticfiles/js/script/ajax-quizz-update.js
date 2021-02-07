define(['jquery',  'bootstrap' ], function ($) {
    $(document).ready(function () {
 
 
    console.log(" ajax-quizz-update chargé ");
 
    qtype = $("#qtype").val() ;

    console.log(qtype);
    // if (qtype == 0)
    // {
    //        var arr = [0,1];  
    //         $.each(arr , function (index, value){

    //         index = index.toString() ; 
    
    //         if ($("#id_choices-"+index+"-is_correct").is(":checked"))
    //             {
    //                 $("#noCheck"+index).hide() ;
    //                 $("#check"+index).show() ;
    //             }
    //         else
    //             {
    //                 $("#noCheck"+index).show() ;
    //                 $("#check"+index).hide() ;
    //             }
    //         });
    // }
    // else if (qtype > 2)
    // {
    //        var arr = [0,1,2,3];  
    //         $.each(arr , function (index, value){

    //         index  =  index.toString()

    //         $("#id_choices-"+index+"-answer").css(value);


    //         if ($("#id_choices-"+index+"-is_correct").is(":checked"))
    //             {
    //                 $("#noCheck"+index).hide() ;
    //                 $("#check"+index).show() ;
    //             }
    //         else
    //             {
    //                 $("#noCheck"+index).show() ;
    //                 $("#check"+index).hide() ;
    //             }
    //         });

    //        var arra = ["bgcolorRed","bgcolorBlue","bgcolorOrange","bgcolorGreen"] ;  
    //         $.each(arra , function (index, value){ console.log(value) ;

    //             index  =  index.toString()
    //             $("#answer"+index+"_div").addClass(value);

    //         });

    // }


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