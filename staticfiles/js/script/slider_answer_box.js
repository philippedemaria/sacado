define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () { 
        console.log("chargement JS ajax-check_pairs.js  OKK");

 
    // ****************************************************************************************************************************************
    // Gestion des slides dans la vue élève
    // ****************************************************************************************************************************************
    
    var div_width = $('#body_zone_exercise').width() ;
    var div_height = $('#body_zone_exercise').height() ;

    var this_slideBox = $('.this_slider ul');

    var slideWidth  = Math.floor(div_width);
    var slideHeight = Math.floor(div_height);

    $(".wrapper_this_slider").width(slideWidth) ;
    $(".this_slide").width(slideWidth-40) ;

    $(".show_correction").width(slideWidth-40) ; 
    $(".show_correction").height(slideHeight) ;



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

    $(".this_slider").removeClass('no_visu_on_load') ; 




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





        $('body').on('change', "#customRange", function (e) {
            idx  = $("#customRange").val() ; 

            sizes = [20,24,28,32,36,40];
            lines = [25,30,35,40,45,50];
            inputs = [22,24,28,32,36,40];

            $(".consigne").attr("style","line-height:"+lines[idx]+"px;font-size:"+sizes[idx]+"px");
            $(".input_latex").attr("style","font-size:"+inputs[idx]+"px");
        });






});

});
