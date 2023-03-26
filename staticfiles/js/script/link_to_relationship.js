define(['jquery', 'bootstrap', 'ui', 'ui_sortable'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-bibiotex.js OK");

  
      
    $('body').on('click', '.image_parcours_link_exotex', function () {

            var exotex_id = $(this).data("id"); 
            var this_exotex = $("#to_link"+exotex_id) ; 

            if (this_exotex.is(":checked")){

                this_exotex.prop('checked', false);
                $("#image_link"+exotex_id).removeClass('image_parcours_link_exotex_selected') ;
            }
            else
            {
                this_exotex.prop('checked', true);
                $("#image_link"+exotex_id).addClass('image_parcours_link_exotex_selected') ; 
            }

   });
 

});
});

