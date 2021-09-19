define(['jquery','bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-parcours-complement.js OK");
 

        $("#id_is_publish").on('change', function (event) {
            $('.publication_div').toggle(500);
        });

       
        $('#id_is_favorite').prop('checked', true); 

        $('#id_zoom').prop('checked', false); 
 
        $('#id_is_publish').prop('checked', false); 
        $('#id_is_achievement').prop('checked', false); 


        $('#id_is_task').prop('checked', false); 
        $('#id_is_paired').prop('checked', false); 
        $('#id_notification').prop('checked', false); 
 
        $('#id_is_leaf').prop('checked', false); 


        $('#folder_parcours').hide(); 
        $('#folder_parcours_cible').hide(); 

        $("#id_is_leaf").on('change', function (event) {
            $('#folder_parcours_cible').toggle(500);
        });


        // Pour le form_parcours
 
         $('#folder_div').hide(); 



         $('#leaf_div').hide(); 



    });
});