define(['jquery', 'bootstrap', 'ui', 'ui_sortable'], function ($) {
    $(document).ready(function () { 
        console.log("chargement JS ajax-check_regroup.js  OKK");

 
    // ****************************************************************************************************************************************
    // Gestion des slides dans la vue élève
    // ****************************************************************************************************************************************
    var this_slideBox = $('.this_slider ul');
    var slideWidth = 700 ;
    var slideQuantity = $('.this_slider ul').children('li').length;
    var currentSlide = 1 ;
    this_slideBox.css('width', slideWidth*slideQuantity);
    var nb_variables = $('#nb_variables').length; 

    //setTimeout( function() { set_var_value(1) }, 1000);


    $('.nav_start').on('click', function(){ 

        var pxValue = currentSlide * slideWidth ; 
        this_slideBox.animate({
            'left' : -pxValue
        });
        currentSlide++ ;
    });


    //===========================================================================================   
    //=========================      DRAG & DROP      ===========================================
    //===========================================================================================  

    var card_ids = [] ; 
    $(document).on('click','.card', function(e) {  
            
            let length     = $("#length").val(); 
            $(this).toggleClass('is-flipped');
            card_ids.push( $(this).data('id') ) ;

            if (card_ids.length == length){ setTimeout(function() {  test_ajax_memo(card_ids,length)}  , 1000) ;  }
                            
        }) 

    function test_ajax_memo(liste,length){

            let csrf_token  = $("input[name='csrfmiddlewaretoken']").val();
            let numexo      = $("#numexo").val();
            let score       = $("#score").val() ;

                $.ajax({
                        type: "POST",
                        dataType: "json",
                        traditional : true,
                        data: {
                            'liste' : liste,
                            'length': length,
                            csrfmiddlewaretoken: csrf_token,
                        },
                        url: "../../ajax_memo",
                        success: function (data) {

                              

                            if (data.test == "yes")
                            {
                                
                                $("#score_span").text( parseInt(score) + 1 );
                                $("#score").val( parseInt(score) + 1 );

                                $(".card").each( function(index) {
                                    if ( $(this).hasClass('is-flipped') ){
                                        $(this).addClass('card_open'); 
                                    }
                                })

                            }
                            else
                            {
                                $(".card").each( function(index) {
                                    if ( $(this).hasClass('is-flipped') ){
                                        $(this).removeClass('is-flipped');

                                    }
                                })
                            }
                            card_ids = [] ; console.log(card_ids) ;
                            $("#numexo_span").text( parseInt(numexo) + 1 );
                            $("#numexo").val( parseInt(numexo) + 1 );
                        }
                    }) 
    }



//*************************************************************************************************************  
// Récupération des réponses
//************************************************************************************************************* 

    $(document).on('change', ".selected_answer" , function () { 

        let csrf_token     = $("input[name='csrfmiddlewaretoken']").val();
        let is_correct     = $(this).data("is_correct") ;
        let loop           = $(this).data("loop") ;
        let choice_id      = $(this).val() ;
        let list_choices   = [] ;   
             
        if ($(this).is(":checked"))
        {
            list_choices.push(choice_id) ;
        }
        else{

            idx = list_choices.indexOf(  choice_id ) ;
            if(idx>-1)
            { list_choices.splice(idx, 1) ;}
        }
        $("#nav_start"+loop).attr("data-choice_ids",list_choices);;
        $("#nav_start"+loop).attr("data-is_correct",is_correct);
    });




 
    });

});

 
