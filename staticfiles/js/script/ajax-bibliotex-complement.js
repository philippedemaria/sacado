define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-bibiotex.js OK");

        $('.publication_div').hide();
        $("#id_is_publish").on('change', function (event) {
            $('.publication_div').toggle(500);
        });
 
        $('#id_is_publish').prop('checked', true); 
 
         $('#id_is_share').prop('checked', true); 

         $('#id_is_archive').prop('checked', false); 
 

});

});

