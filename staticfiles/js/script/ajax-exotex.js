define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-exercise.js OK");



        $('[type=checkbox]').prop('checked', false);            

        $('#id_is_publish').prop('checked', true);
        $('#id_is_share').prop('checked', true);  
        $("#publication_div").hide();
 

            makeDivAppear($("#id_is_publish"), $("#publication_div"));


            function makeDivAppear($toggle, $item) {
                    $toggle.change(function () {
                         $item.toggle();
                    });
                }
 

        $('#enable_correction_div').hide();
        $("#enable_correction").click(function(){ 
            $('#enable_correction_div').toggle(500);
        });



});

});

