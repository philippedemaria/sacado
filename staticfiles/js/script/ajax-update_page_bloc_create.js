define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-update_page_bloc_create.js OK");

        $('#id_is_calculator').prop('checked', false); 
 
        $('#id_is_python').prop('checked', true); 
 
        $('#id_is_scratch').prop('checked', true); 

        $('#id_is_tableur').prop('checked', false); 

        $('#id_is_annals').prop('checked', false); 
    });

});

 