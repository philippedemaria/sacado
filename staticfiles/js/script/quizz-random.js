define(['jquery',  'bootstrap' ], function ($) {
    $(document).ready(function () {
 
 
    console.log("  quizz-random chargé ");
 
 


        $('.selector_w').on('click', function(){

                let w_id = $(this).attr("data-id");
                $(".open").prop("checked",false) ; 

                if ($('.selector_w').is(":checked"))
                {
                    $(".kw"+w_id).prop("checked",true) ;
                }
                else{
                    $(".kw"+w_id).prop("checked",false) ;                    
                }



            })  
 



    });
});