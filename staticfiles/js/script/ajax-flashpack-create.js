define(['jquery', 'bootstrap', 'ui', 'ui_sortable'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-flashpack.js OK");

        $('#id_themes_div').hide();

        $('#id_is_publish').prop('checked', true);
        $('#id_is_archive').prop('checked', false); 
        $('#id_is_creative').prop('checked', false); 
        $('#id_is_global').prop('checked', false);




        

        $('#id_is_global').on('change', function (event) {
 
    		if ($('#id_is_global').is(":checked")) { 

   				alert("En cochant Flashpack annuel, vous annulez les choix sur les dossiers et les parcours. " ) ;     			
    			
    			}

    			$('.select_folders').prop('checked', false); 
    			$('.select_all_parcours').prop('checked', false); 

    			$('#creative_is_global').toggle() ;
    			$('#stop_is_global').toggle() ;
    			$('#themes_is_global').toggle() ;
    			$('#folders_is_global').toggle() ;
 
        })
 

});

});

