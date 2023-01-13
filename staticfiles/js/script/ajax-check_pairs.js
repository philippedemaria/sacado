define(['jquery', 'bootstrap', 'ui', 'ui_sortable'], function ($) {
    $(document).ready(function () { 
        console.log("chargement JS ajax-check_pairs.js  OKK");

 
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
    //=========================      PAIRES      ================================================  
    //===========================================================================================  

    $( document ).on('mouseover', ".draggable" , function () { 
        var loop = $(this).data('loop');
        $( this ).draggable({
                containment: ".dropzone"+loop ,
                appendTo : '.droppable'+loop , 
                revert : true,
            });

        $( ".droppable"+loop ).droppable({
                drop: function( event, ui ) {

                    $(this).append( $(ui.draggable[0])  );
                    this_answer = $(ui.draggable[0]).data("subchoice") ;
                    old_list = $(this).find('input').val()  ;  
                    var new_list = [];
                    var new_str  = old_list +this_answer+"----";
                    $(this).find('input').val(new_str);
                    $('.quizz_item').css('border', '1px solid #E0E0E0');
                },
                over: function(event, ui) {
                    $(this).css('border', '2px solid green');
                },
                out: function(event, ui) {

                    this_answer = $(ui.draggable[0]).data("subchoice") ;
                    old_list = $(this).find('input').val()  ;  
                    var new_list = [];
                    var new_str  = old_list.replace(this_answer+"----", "");
                    $(this).find('input').val(new_str);
                     $(this).css('border', '1px solid #E0E0E0');
                }
        });

    })



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





//*************************************************************************************************************  
// Correction des paires
//*************************************************************************************************************  
    $(document).on('click', ".show_these_pairs_correction" , function () {

 
            let listing = [] ; 


            event.preventDefault();   
            my_form = document.querySelector("#all_types_form");
            var form_data = new FormData(my_form); 
 
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            let supportfile_id = $(this).data("supportfile_id") ;
            let loop           = $(this).data("loop") ;

            form_data.append("csrfmiddlewaretoken" , csrf_token);
            form_data.append("supportfile_id" , supportfile_id); 
            form_data.append("loop" , loop);  


            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    traditional : true,
                    data: form_data,
                    url: "../../check_solution_pairs",
                    success: function (data) {
                        $("#score").val(data.score);
                        $("#numexo").val(data.numexo);
                        $("#score_span").html(data.score);
                        $("#numexo_span").html(data.numexo);
                        //********** Gestion de la div de solution ********************
                        $("#show_correction"+loop).show(500);
                        $("#this_correction_text"+loop).html(data.this_correction_text);
                        $("#message_correction"+loop).html(data.msg);
                        //*************************************************************
                        MathJax.Hub.Queue(["Typeset",MathJax.Hub]);    
                    },
                        cache: false,
                        contentType: false,
                        processData: false
                }
            )
         });
    });

});

 
