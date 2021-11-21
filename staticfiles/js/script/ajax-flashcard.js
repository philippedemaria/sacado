define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-flashcard.js OK");

  



        $("#this_answer_textarea_display").click(function(){ 
            var value = CKEDITOR.instances['id_answer'].getData();
            $('#type_of_textarea_display').html("la réponse");
            $('#body_of_textarea_display').html(value);
            
        });

         
        $("#this_question_textarea_display").click(function(){ 
            var value = CKEDITOR.instances['id_question'].getData();
            $('#type_of_textarea_display').html("la question");
            $('#body_of_textarea_display').html(value);
            
        });


 
        $("#this_helper_textarea_display").click(function(){ 
            var value = CKEDITOR.instances['id_helper'].getData();
            $('#type_of_textarea_display').html("l'aide");
            $('#body_of_textarea_display').html(value);
            
        });





});

});

