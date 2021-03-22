define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-exercise.js OK");


 
        $('[type=checkbox]').prop('checked', false);            

        $('#selector_student').prop('checked', true);
        $('.selected_student').prop('checked', true);

        $('#id_is_publish').prop('checked', true);

        $('#id_is_ggbfile').prop('checked', true); 


        $('#on_mark').hide(); 


 
        $("#click_button").on('click', function (){ 

            if (!$('#id_is_ggbfile').is(":checked")){

                if (!$('#id_is_realtime').is(":checked") && !$('#id_is_python').is(":checked") && !$('#id_is_scratch').is(":checked") && !$('#id_is_file').is(":checked") && !$('#id_is_image').is(":checked") && !$('#id_is_text').is(":checked"))
                { alert("vous devez sélectionner une type de remise d'exercice") ; return false ; } 
            } 
            else
            {
                if ($("#id_ggbfile").val() == "") { alert("vous devez uploader un ficher GGB") ; return false ;}
            }

        });



});

});

