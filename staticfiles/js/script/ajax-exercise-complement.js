define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-exercise.js OK");


 
            $('[type=checkbox]').prop('checked', false);            

            $('#selector_student').prop('checked', true);
            $('.selected_student').prop('checked', true);

            $('#id_is_publish').prop('checked', true);

            $('#id_is_ggbfile').prop('checked', true);            
 
        $("#click_button").click(function(){ 

            if (!$('#id_is_python').is(":checked") && !$('#id_is_scratch').is(":checked") && !$('#id_is_file').is(":checked") && !$('#id_is_image').is(":checked") && !$('#id_is_text').is(":checked"))
            { alert("vous devez sélectionner une type de remise d'exercice") ; return false ; } 
        });

});

});

