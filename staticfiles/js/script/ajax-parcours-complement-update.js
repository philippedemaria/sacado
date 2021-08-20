define(['jquery','bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-parcours-complement-update.js OK");
 
 
 

        $("#id_is_leaf").on('change', function (event) {
            $('#folder_parcours_cible').toggle(500);
        });

 
        
        if ($('#id_is_leaf').is(':checked')) 
            { $('#folder_parcours_cible').show();  }
        else 
            { $('#folder_parcours_cible').hide();  }

    });
});