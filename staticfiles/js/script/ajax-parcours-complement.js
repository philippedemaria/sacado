define(['jquery','bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-parcours-complement.js OK");
 

        $("#id_is_publish").on('change', function (event) {
            $('#publication_div').toggle(500);
        });


        $('[type=checkbox]').prop('checked', false);        


    });
});